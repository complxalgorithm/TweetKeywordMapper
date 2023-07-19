
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
    
    # ask user for name of US states shp directory
    shp_dir = input('Enter directory name to put shapefile in: ')
    
    # validate that there is no space in shp_dir value
    while ' ' in shp_dir:
        print('ERROR - There is a space in that value.')
        
        # ask user again for name of US states shp directory
        shp_dir = input('Enter directory name to put shapefile in: ')
    
    # set path to new directory
    shp_path = os.path.join(ws, shp_dir)
    
    # set link to shapefile from US Census Bureau website
    shp_url = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_5m.zip'
    
    # get shapefile name from shp_url
    file_name = os.path.splitext(os.path.basename(shp_url))[0]
    
    # try to make the new directory
    try:
        os.mkdir(shp_path)
    
    except Exception:
        print(f'{shp_path} already exists.\n')
    
    else:
        print(f'{shp_path} created successfully.\n')
    
    time.sleep(0.5)     # pause program for half a second
    
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