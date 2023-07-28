"""
# define download_shp() function - download US State boundaries shapefile from US Census Bureau website
"""
def download_shp(ws):
    # import modules
    import os
    import time
    from io import BytesIO
    from urllib.request import urlopen
    from zipfile import ZipFile
    
    # set link to shapefile from US Census Bureau website
    shp_url = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_5m.zip'
    
    ##get shapefile name from shp_url
    ##file_name = os.path.splitext(os.path.basename(shp_url))[0]
    
    # ask user for name of US states shp directory
    shp_dir = input('Enter directory name to put shapefile in: ')
    
    # set path to new directory
    shp_path = os.path.join(ws, shp_dir)
    
    # validate that there is no space in shp_dir value, and that shp_path does not already exist
    while ' ' in shp_dir or os.path.exists(shp_path):
        if ' ' in shp_dir:
            print('\nERROR - There is a space in that value.')
        
        else:
            print(f'\nERROR - {shp_path} already exists.')
        
        # ask user again for name of US states shp directory
        shp_dir = input('\nEnter directory name to put shapefile in: ')
        
        # set new path to new directory
        shp_path = os.path.join(ws, shp_dir)
    
    # try to make the new directory
    try:
        os.mkdir(shp_path)
    
    except Exception:
        print(f'\nSomething went wrong when attempting to create {shp_path}.\n')
    
    else:
        print(f'\n{shp_path} created successfully.\n')
    
    time.sleep(1)     # pause program for a second
    
    # try to download shapefile zip and extract files
    try:
        print(f'Attempting to download US States shapefile into {shp_path}.....\n')
        time.sleep(1.5)     # pause program for a second and a half
        
        # CREDIT: Drakax - https://stackoverflow.com/questions/72502959/download-zip-file-from-url-using-python
        with urlopen(shp_url) as zip_resp:
            with ZipFile(BytesIO(zip_resp.read())) as zipfile:
                zipfile.extractall(shp_path)
    
    except Exception:
        print('ERROR - Something went wrong when attempting to download US States shapefile.\n')
    
    else:
        print(f'US State boundaries shapefile downloaded successfully to {shp_path}')
    
    time.sleep(1)   # pause program for a second
    
    return