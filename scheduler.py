import win32com.client

def create_task(python_path, working_dir):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    triggers = task_def.Triggers
    start_time = "2022-07-04T00:00:00"

    TriggerTypeDaily = 2
    trigger = triggers.Create(TriggerTypeDaily)
    trigger.StartBoundary = start_time

    TriggerTypeRegistration = 7
    trigger = triggers.Create(TriggerTypeRegistration)
    trigger.StartBoundary = start_time
    trigger.Id = "RegistrationTriggerId"
    
    # DOESNT WORK. ERROR - ACCESS DENIED
    # TriggerTypeLogon = 9
    # trigger = triggers.Create(TriggerTypeLogon)
    # trigger.StartBoundary = start_time
    # trigger.Id = "LogonTriggerId"

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = 'TRIGGER BATCH'
    action.Path = python_path
    action.WorkingDirectory = working_dir
    action.Arguments ='main.py'

    # Set parameters
    task_def.RegistrationInfo.Description = 'A recurring daily task that runs the program at midnight. Check https://github.com/mukundhk/Countdown-Wallpaper for more information.'
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    TASK_INSTANCES_STOP_EXISTING = 3 
    task_def.Settings.MultipleInstances = TASK_INSTANCES_STOP_EXISTING

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        'Countdown Wallpaper',  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE
    )