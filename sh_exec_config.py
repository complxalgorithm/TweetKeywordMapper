import os, psutil, time

# list of valid shells
shells = ['sh', 'bash', 'zsh', 'csh', 'ksh', 'fish']

# get parent process name
parent_proc = psutil.Process(os.getppid()).name()
print(f'Shell: {parent_proc}')
time.sleep(1)   # pause for a second

if parent_proc in shells:
    try:
        os.system('chmod +x tkm && chmod +x test')
    except Exception:
        print('Something went wrong when attempting to make tkm and test scripts executable.')
    else:
        print('tkm and test shell scripts are now executable.')
else:
    print(f'{parent_proc} is not a compatible shell.')