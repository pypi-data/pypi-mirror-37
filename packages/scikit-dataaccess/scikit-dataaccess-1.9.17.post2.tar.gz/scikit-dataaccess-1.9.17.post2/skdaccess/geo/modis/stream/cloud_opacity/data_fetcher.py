from skdaccess.geo.modis.stream import DataFetcher as MDF


class DataFetcher(MDF):
    '''
    Data Fetcher for MODIS Cloud Opacity
    '''
    
    def __init__(self, ap_paramList, start_date, end_date, modis_platform = 'Terra',
                 daynightboth = 'D', grid=None):
        '''
        Construct Data Fetcher object for MODIS cloud Opacity data
        
        @param ap_paramList[lat]: Search latitude
        @param ap_paramList[lon]: Search longitude
        @param start_date: Starting date
        @param end_date: Ending date
        @param modis_platform: Paltform (Either "Terra" or "Aqua")
        @param daynightboth: Use daytime data ('D'), nighttime data ('N') or both ('B')
        @param grid: Further divide each image into a multiple grids of size (y,x)
        '''

        super(DataFetcher, self).__init__(ap_paramList, modis_platform, '06_L2', ['Cloud_Optical_Thickness'], start_date, end_date,
                                          daynightboth, grid, use_long_name=False)

