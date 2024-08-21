import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        if result.stderr.strip() == "":
            return "Error: No error message provided."
        return f"Error: {result.stderr}"
    elif result.stdout.strip() == "":
        return "No output returned."
    return result.stdout


def process_check():
    output = {}

    output['top_processes'] = run_command('top -b -n 1')
    output['process_tree'] = run_command('ps -auxwf')
    netstat_output = run_command('netstat -nalp')
    if "Error" in netstat_output:
        output['ss'] = run_command('ss -a -e -i')
    else:
        output['netstat'] = netstat_output

    output['deleted_executables'] = run_command('ls -alR /proc/*/exe 2> /dev/null | grep deleted')

    pids = run_command('ls /proc | grep "^[0-9]"').splitlines()
    for pid in pids:
        output[f'process_{pid}'] = {}
        output[f'process_{pid}']['command_name'] = run_command(f'strings /proc/{pid}/comm')
        output[f'process_{pid}']['cmdline'] = run_command(f'strings /proc/{pid}/cmdline')
        output[f'process_{pid}']['real_path'] = run_command(f'ls -al /proc/{pid}/exe')
        output[f'process_{pid}']['environment'] = run_command(f'strings /proc/{pid}/environ')
        output[f'process_{pid}']['working_directory'] = run_command(f'ls -alR /proc/{pid}/cwd')

        tmp_processes = run_command(f'ls -alR /proc/{pid}/cwd 2> /dev/null | grep tmp')
        dev_processes = run_command(f'ls -alR /proc/{pid}/cwd 2> /dev/null | grep dev')

        if "Error" in tmp_processes:
            output[f'process_{pid}']['tmp_dev_processes'] = f"Error in tmp check: {tmp_processes}"
        elif "Error" in dev_processes:
            output[f'process_{pid}']['tmp_dev_processes'] = f"Error in dev check: {dev_processes}"
        elif tmp_processes.strip() == "" and dev_processes.strip() == "":
            output[f'process_{pid}']['tmp_dev_processes'] = "No tmp or dev processes found."
        else:
            output[f'process_{pid}'][
                'tmp_dev_processes'] = f"tmp processes:\n{tmp_processes}\ndev processes:\n{dev_processes}"

    return output