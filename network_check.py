import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout


def network_check():
    output = {}

    netstat_output = run_command('netstat -nap')
    if "Error" in netstat_output:
        output['ss'] = run_command('ss -tuln')
    else:
        output['netstat'] = netstat_output

    output['promiscuous_mode'] = run_command('ip link | grep PROMISC')
    output['arp_table'] = run_command('ip neigh')

    return output
