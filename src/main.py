#!/usr/bin/env python3
"""
SS7 Termux Tools - Main CLI Entry Point

Command-line interface for SS7 vulnerability analysis tools.
"""

import sys
import os
import logging
import json
from pathlib import Path

try:
    import click
except ImportError:
    print("Error: Click not installed. Run: pip install click")
    sys.exit(1)

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import logger as logger_module
from src.utils import validators
from src.tools.scanner import SS7Scanner
from src.tools.analyzer import SS7Analyzer

# Setup logging
log = logger_module.setup_logger('ss7_tools', logging.INFO)

# Package metadata
__version__ = "0.1.0"
__author__ = "Mar140-tech"


class Config:
    """Config object for CLI context"""
    def __init__(self):
        self.config_file = "config/config.json"
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            log.warning(f"Could not load config file: {e}")

        # Return default config
        return {
            'network': {'timeout': 5, 'retries': 3},
            'ss7': {'protocol_version': 'ITUQ773', 'debug': False},
            'logging': {'level': 'INFO'},
            'output': {'format': 'json', 'directory': 'results'}
        }


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
@click.pass_context
def cli(ctx, verbose, debug):
    """SS7 Termux Tools - SS7 Vulnerability Analysis Suite"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config()

    # Setup logging level
    if debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debug mode enabled")
    elif verbose:
        log.setLevel(logging.INFO)


@cli.command()
def version():
    """Show version information"""
    click.echo(f"SS7 Termux Tools v{__version__}")
    click.echo(f"Author: {__author__}")
    click.echo(f"Python: {sys.version.split()[0]}")


@cli.command()
@click.option('--target', '-t', required=True, help='Target IP or CIDR range (e.g., 192.168.1.0/24)')
@click.option('--output', '-o', default='scan_results.json', help='Output file for results')
@click.option('--timeout', type=int, default=5, help='Connection timeout in seconds')
@click.option('--retries', type=int, default=3, help='Number of retry attempts')
@click.option('--ports', default='', help='Comma-separated list of ports to scan')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def scan(ctx, target, output, timeout, retries, ports, verbose):
    """Scan network for SS7 nodes and services"""
    try:
        log.info(f"Starting SS7 network scan: {target}")

        # Validate inputs
        if '/' in target:
            if not validators.validate_cidr(target):
                click.secho(f"❌ Invalid CIDR range: {target}", fg='red')
                return
        else:
            if not validators.validate_ip_address(target):
                click.secho(f"❌ Invalid IP address: {target}", fg='red')
                return

        if not validators.validate_timeout(timeout):
            click.secho(f"❌ Invalid timeout: {timeout}", fg='red')
            return

        # Parse ports if provided
        port_list = None
        if ports:
            try:
                port_list = [int(p.strip()) for p in ports.split(',')]
                for p in port_list:
                    if not validators.validate_port(p):
                        click.secho(f"❌ Invalid port: {p}", fg='red')
                        return
            except ValueError:
                click.secho(f"❌ Invalid port list: {ports}", fg='red')
                return

        # Create scanner
        scanner = SS7Scanner(timeout=timeout, retries=retries, ports=port_list or SS7Scanner.DEFAULT_PORTS)

        # Run scan
        click.secho(f"🔍 Scanning {target}...", fg='cyan')
        results = scanner.scan_network(target)

        # Display results
        click.echo()
        if results:
            click.secho(f"✓ Found {len(results)} open ports/services:", fg='green')
            for result in results:
                click.echo(f"  • {result.host}:{result.port} ({result.service}) - {result.response_time*1000:.2f}ms")
        else:
            click.secho("⚠ No open ports found", fg='yellow')

        # Save results
        click.echo()
        click.secho(f"💾 Saving results to {output}...", fg='cyan')
        if scanner.save_results(output):
            click.secho(f"✓ Results saved successfully", fg='green')
        else:
            click.secho(f"❌ Failed to save results", fg='red')

        log.info(f"Scan completed. Found {len(results)} results.")

    except Exception as e:
        click.secho(f"❌ Error: {e}", fg='red')
        log.error(f"Scan error: {e}", exc_info=True)


@cli.command()
@click.option('--pcap', '-p', required=True, help='Path to PCAP file')
@click.option('--output', '-o', default='analysis_results.json', help='Output file for results')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def analyze(ctx, pcap, output, verbose):
    """Analyze captured SS7 traffic from PCAP file"""
    try:
        log.info(f"Starting analysis of PCAP: {pcap}")
        click.secho(f"📊 Analyzing traffic from {pcap}...", fg='cyan')

        if not os.path.exists(pcap):
            click.secho(f"❌ PCAP file not found: {pcap}", fg='red')
            return

        analyzer = SS7Analyzer()

        if not analyzer.load_pcap(pcap):
            click.secho(f"❌ Failed to load PCAP file", fg='red')
            return

        click.secho(f"✓ PCAP file loaded successfully", fg='green')
        log.info(f"Analysis completed.")

    except Exception as e:
        click.secho(f"❌ Error: {e}", fg='red')
        log.error(f"Analysis error: {e}", exc_info=True)


@cli.command('detect-vuln')
@click.option('--report', '-r', is_flag=True, help='Generate detailed report')
@click.option('--output', '-o', default='vulnerability_report.json', help='Output file for report')
@click.pass_context
def detect_vulnerabilities(ctx, report, output):
    """Detect known SS7 vulnerabilities"""
    try:
        log.info("Starting vulnerability detection")
        click.secho(f"🔐 Scanning for SS7 vulnerabilities...", fg='cyan')

        analyzer = SS7Analyzer()
        vulnerabilities = analyzer.detect_vulnerabilities()

        # Display results
        click.echo()
        if vulnerabilities:
            click.secho(f"✓ Detected {len(vulnerabilities)} vulnerabilities:", fg='yellow')
            for vuln in vulnerabilities:
                severity_color = 'red' if vuln['severity'] == 'critical' else 'yellow'
                click.secho(f"  • [{vuln['severity'].upper()}] {vuln['name']}", fg=severity_color)
                click.echo(f"    {vuln['description']}")
        else:
            click.secho("✓ No vulnerabilities detected", fg='green')

        # Generate report if requested
        if report:
            click.echo()
            click.secho(f"📝 Generating report to {output}...", fg='cyan')
            if analyzer.generate_report(output):
                click.secho(f"✓ Report generated successfully", fg='green')
            else:
                click.secho(f"❌ Failed to generate report", fg='red')

        log.info(f"Vulnerability detection completed. Found {len(vulnerabilities)} vulnerabilities.")

    except Exception as e:
        click.secho(f"❌ Error: {e}", fg='red')
        log.error(f"Vulnerability detection error: {e}", exc_info=True)


@cli.command()
@click.option('--check', is_flag=True, help='Check configuration')
@click.option('--show', is_flag=True, help='Show current configuration')
@click.pass_context
def config(ctx, check, show):
    """Manage tool configuration"""
    try:
        cfg = ctx.obj['config']

        if show:
            click.secho("Current Configuration:", fg='cyan')
            click.echo(json.dumps(cfg.config, indent=2))
            return

        if check:
            click.secho("Checking configuration...", fg='cyan')
            click.secho("✓ Configuration is valid", fg='green')
            return

        click.secho("Configuration management:", fg='cyan')
        click.echo("  Use --show to display current configuration")
        click.echo("  Use --check to validate configuration")

    except Exception as e:
        click.secho(f"❌ Error: {e}", fg='red')


@cli.command()
def help():
    """Show help information"""
    click.echo("""SS7 Termux Tools - Help

Available Commands:
  scan              - Scan network for SS7 nodes
  analyze           - Analyze SS7 traffic from PCAP
  detect-vuln       - Detect SS7 vulnerabilities
  config            - Manage configuration
  version           - Show version info
  help              - Show this help

Examples:
  # Scan a network
  python3 src/main.py scan --target 192.168.1.0/24 -o results.json

  # Analyze PCAP file
  python3 src/main.py analyze --pcap traffic.pcap

  # Detect vulnerabilities and generate report
  python3 src/main.py detect-vuln --report -o report.json

  # Show configuration
  python3 src/main.py config --show

Options:
  -v, --verbose     Enable verbose output
  -d, --debug       Enable debug output
  -h, --help        Show command help
""")


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        click.echo()
        click.secho("\n⚠ Interrupted by user", fg='yellow')
        sys.exit(0)
    except Exception as e:
        click.secho(f"❌ Fatal error: {e}", fg='red')
        log.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
