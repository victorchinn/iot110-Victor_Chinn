#!/usr/bin/python
import serial
import pynmea2

#globals

# for Raspberry Pi 3 - must execute command:
# sudo systemtl stop serial-getty@ttyS0 
# before running this program

def read_serial_gps (numsentences):
    # read the serial port for the number of sentences specified
    # to hold data for GPS 
    lat = 0 
    lon = 0
    alt = 0
    numsats = 0 
    speed = 0
    serial_data_line = ""
    
    with serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1) as ser:
    #with serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1) as ser:
        # read 10 lines or WHILE loop to read data from the /dev/ttyS0 GPS on the UART
        for num in range(numsentences):
            try:
                serial_data_line = ser.readline().decode('ascii', errors='replace')
                GPS_Line = serial_data_line.strip(' ')
                #print "Read :", GPS_Line   

            except Exception as e:
                #print "serial port exception"
                #ignored
                pass

            try:
                #decoded = pynmea2.parse(' $GPRMC,223114.000,A,4733.8824,N,12206.4382,W,0.06,275.93,050317,,,A*78')
                #decoded = pynmea2.parse(' $GPVTG,32.80,T,,M,0.08,N,0.16,K,A*0B')
                #decoded = pynmea2.parse(' $GPGGA,032222.000,4733.8736,N,12206.4312,W,1,08,0.85,214.3,M,-17.3,M,,*5E')

                # check the first 6 characters of the input data line from the GPS to see how to parse it
                GPS_Prefix = GPS_Line[0:6]
                if (GPS_Prefix == '$GPGSA'):
                    #class GPGSA(NMEASentence):
                    #    def __init__(self):
                    #        parse_map = (
                    #            ('Mode', 'mode'),
                    #            ('Mode fix type', 'mode_fix_type'),
                    #            ('SV ID01', 'sv_id01'),
                    #            ('SV ID02', 'sv_id02'),
                    #            ('SV ID03', 'sv_id03'),
                    #            ('SV ID04', 'sv_id04'),
                    #            ('SV ID05', 'sv_id05'),
                    #            ('SV ID06', 'sv_id06'),
                    #            ('SV ID07', 'sv_id07'),
                    #            ('SV ID08', 'sv_id08'),
                    #            ('SV ID09', 'sv_id09'),
                    #            ('SV ID10', 'sv_id10'),
                    #            ('SV ID11', 'sv_id11'),
                    #            ('SV ID12', 'sv_id12'),
                    #            ('PDOP (Dilution of precision)', 'pdop'),
                    #            ('HDOP (Horizontal DOP)', 'hdop'),
                    #            ('VDOP (Vertical DOP)', 'vdop'))
                    #            #('Checksum', 'checksum'))
                    #
                    #        super(GPGSA, self).__init__(parse_map)
                    decoded = pynmea2.parse(GPS_Line) 

                elif (GPS_Prefix == '$GPRMC'):
                    #class GPRMC(NMEASentence):
                    #    """ Recommended Minimum Specific GPS/TRANSIT Data
                    #    """
                    #    def __init__(self):
                    #        parse_map = (("Timestamp", "timestamp"),
                    #                     ("Data Validity", "data_validity"),
                    #                     ("Latitude", "lat"),
                    #                     ("Latitude Direction", "lat_dir"),
                    #                     ("Longitude", "lon"),
                    #                     ("Longitude Direction", "lon_dir"),
                    #                     ("Speed Over Ground", "spd_over_grnd"),
                    #                     ("True Course", "true_course"),
                    #                     ("Datestamp", "datestamp"),
                    #                     ("Magnetic Variation", "mag_variation"),
                    #                     ("Magnetic Variation Direction", "mag_var_dir"))
                    #                     #("Checksum", "checksum"))
                    #        super(GPRMC, self).__init__(parse_map)
                    decoded = pynmea2.parse(GPS_Line) 
           
                    #print "LAT:", decoded.lat,
                    #print "LON:", decoded.lon
                    lat = decoded.lat
                    lon = decoded.lon

                elif (GPS_Prefix == '$GPVTG'):
                    #    class GPVTG(NMEASentence):
                    #    """ Track Made Good and Ground Speed
                    #    ("True Track made good", "true_track"),
                    #    ("True Track made good symbol", "true_track_sym"),
                    #    ("Magnetic Track made good", "mag_track"),
                    #    ("Magnetic Track symbol", "mag_track_sym"),
                    #    ("Speed over ground knots", "spd_over_grnd_kts"),
                    #    ("Speed over ground symbol", "spd_over_grnd_kts_sym"),
                    #    ("Speed over ground kmph", "spd_over_grnd_kmph"),
                    #    ("Speed over ground kmph symbol", "spd_over_grnd_kmph_sym"))
                    decoded = pynmea2.parse(GPS_Line) 

                    #print "SPKM:",decoded.spd_over_grnd_kmph
                    speed = decoded.spd_over_grnd_kmph

                elif (GPS_Prefix == '$GPGGA'):
                    #class GPGGA(NMEASentence):
                    #    def __init__(self):
                    #        parse_map = (
                    #            ('Timestamp', 'timestamp'),
                    #            ('Latitude', 'latitude'),
                    #            ('Latitude Direction', 'lat_direction'),
                    #            ('Longitude', 'longitude'),
                    #            ('Longitude Direction', 'lon_direction'),
                    #            ('GPS Quality Indicator', 'gps_qual'),
                    #            ('Number of Satellites in use', 'num_sats'),
                    #            ('Horizontal Dilution of Precision', 'horizontal_dil'),
                    #            ('Antenna Alt above sea level (mean)', 'antenna_altitude'),
                    #            ('Units of altitude (meters)', 'altitude_units'),
                    #            ('Geoidal Separation', 'geo_sep'),
                    #            ('Units of Geoidal Separation (meters)', 'geo_sep_units'),
                    #            ('Age of Differential GPS Data (secs)', 'age_gps_data'),
                    #            ('Differential Reference Station ID', 'ref_station_id'))
                    #            #('Checksum', 'checksum'))
                    #
                    #        super(GPGGA, self).__init__(parse_map)
                    decoded = pynmea2.parse(GPS_Line)
                    #print "ALT:",decoded.altitude
                    alt = decoded.altitude

                elif (GPS_Prefix == '$GPGSV'):
                    #class GPGSV(NMEASentence):
                    #    def __init__(self):
                    #        parse_map = (
                    #    ('Number of messages of type in cycle', 'num_messages'),
                    #    ('Message Number', 'msg_num'),
                    #    ('Total number of SVs in view', 'num_sv_in_view'),
                    #    ('SV PRN number 1', 'sv_prn_num_1'),
                    #    ('Elevation in degrees 1', 'elevation_deg_1'), # 90 max
                    #    ('Azimuth, deg from true north 1', 'azimuth_1'), # 000 to 159
                    #    ('SNR 1', 'snr_1'), # 00-99 dB
                    #    ('SV PRN number 2', 'sv_prn_num_2'),
                    #    ('Elevation in degrees 2', 'elevation_deg_2'), # 90 max
                    #    ('Azimuth, deg from true north 2', 'azimuth_2'), # 000 to 159
                    #    ('SNR 2', 'snr_2'), # 00-99 dB
                    #    ('SV PRN number 3', 'sv_prn_num_3'),
                    #    ('Elevation in degrees 3', 'elevation_deg_3'), # 90 max
                    #    ('Azimuth, deg from true north 3', 'azimuth_3'), # 000 to 159
                    #    ('SNR 3', 'snr_3'), # 00-99 dB
                    #    ('SV PRN number 4', 'sv_prn_num_4'),
                    #    ('Elevation in degrees 4', 'elevation_deg_4'), # 90 max
                    #    ('Azimuth, deg from true north 4', 'azimuth_4'), # 000 to 159
                    #    ('SNR 4', 'snr_4'))  # 00-99 dB
                    #    #('Checksum', 'checksum'))
                    #
                    #        super(GPGSV, self).__init__(parse_map) 
                    #satellites in view
                    decoded = pynmea2.parse(GPS_Line)
                    #print "#SATS:", decoded.num_sv_in_view
                    numsats = decoded.num_sv_in_view

            except Exception as e:
                print "Error decoding :", serial_data_line
                #so ignore it if cant decode it
                pass

    print "GPS DATA","LAT:",lat ,"LON:",lon,"ALT:",alt,"#NUMSATS:",numsats,"SPEED:",speed
    return lat,lon,alt,numsats,speed  
