
## Command Line Interface

### Prerequisites
* [python 2.7.9+ or 3.4+](https://www.python.org/downloads/)
* [LeoLabs Platform Account](https://platform.leolabs.space/)

### Installation

pip install leolabs --upgrade

### Configuration

```
$ leolabs configure
Access Key: xxxxx
Secret Key: xxxxx
```

### Examples

List Instruments
```
$ leolabs instruments list
{
    "instruments": [
        {
            "altitude": 213.0, 
            "longitude": -147.47104, 
            "latitude": 65.12992, 
            "transmitFrequency": 450000000.0, 
            "id": "pfisr", 
            "transmitPower": 2000000.0
        }, 
        {
            "altitude": 855.0, 
            "longitude": -103.233245, 
            "latitude": 31.9643, 
            "transmitFrequency": 440000000.0, 
            "id": "msr", 
            "transmitPower": 65000.0
        }
    ]
}
```

Get a Catalog Object by LeoLabs Catalog Number
```
$ leolabs catalog get --catalog-number L335
{
    "name": "ENVISAT", 
    "noradCatalogNumber": 27386, 
    "catalogNumber": "L335"
}
```

Get a Catalog Object by Norad Catalog Number
```
leolabs catalog get --norad-catalog-number 27386
{
    "name": "ENVISAT", 
    "noradCatalogNumber": 27386, 
    "catalogNumber": "L335"
}
```

Request Priority Tasking for Catalog Object
```
leolabs catalog create-task --catalog-number L335 \
  --start-time "2017-09-01T03:00:00Z" \
  --end-time "2017-09-01T03:01:00Z"
{
    "id": 27102
}
```

Get Measurements
```
leolabs catalog get-measurements --catalog-number L335 \
  --start-time "2017-08-14T18:59:24Z" \
  --end-time "2017-08-14T18:59:25Z"
{
    "measurements": [
        {
            "group": 1, 
            "noradCatalogNumber": 27386, 
            "beam": 65126, 
            "measuredAt": "2017-08-14T18:59:24.124471", 
            "catalogNumber": "L335", 
            "corrected": {
                "dopplerError": 2.95906889313967, 
                "doppler": -541.573712963274, 
                "elevation": 64.32, 
                "rcs": 0.271515669632799, 
                "rangeError": 14.0771121565189, 
                "range": 844051.73662067, 
                "azimuth": 84.8
            }, 
            "transmittedAt": "2017-08-14T18:59:24.121656", 
            "receivedAt": "2017-08-14T18:59:24.127287", 
            "instrument": "pfisr", 
            "experiment": 4879612, 
            "values": {
                "dopplerError": 37.3883989266642, 
                "doppler": -555.480127498331, 
                "elevation": 64.32, 
                "rcs": 0.000543889663672399, 
                "rangeError": 31.9670816213217, 
                "range": 844063.93383224, 
                "azimuth": 84.8
            }, 
            "integrationTime": 0.0019000000320375, 
            "updatedAt": "2017-08-14T19:05:28.756542", 
            "corrections": [
                {
                    "source": "leolabs", 
                    "type": "doppler_bias", 
                    "value": -13.9064145350566, 
                    "error": 0.0564834780040618
                }, 
                {
                    "source": "leolabs", 
                    "type": "range_bias", 
                    "value": -4.5517080652644, 
                    "error": 0.24854786082094
                }, 
                {
                    "source": "iri16", 
                    "type": "ionospheric", 
                    "value": 16.7489196346786
                }
            ], 
            "snr": 21.9874788479196, 
            "id": 100840433, 
            "targetPass": 89454166
        }
    ]
}
```

List State Vectors
```
leolabs catalog list-states --catalog-number L335 --start-time "2017-11-08T00:00:00Z" --end-time "2017-11-09T00:00:00Z"
or
leolabs catalog list-states --catalog-number L335 --latest 1
{
    "states": [
        {
            "id": 411615, 
            "noradCatalogNumber": 27386, 
            "timestamp": "2017-11-08T03:58:15.386156", 
            "updatedAt": "2017-11-08T05:56:26.801277", 
            "createdAt": "2017-11-08T05:56:26.801291", 
            "catalogNumber": "L335", 
            "frames": {
                "TNW": {
                    "position": [
                        0.0, 
                        0.0, 
                        -0.0
                    ], 
                    "velocity": [
                        0.0, 
                        0.0, 
                        -0.0
                    ]
                    "covarianceExtended": [...],
                    "covariance": [
                        [
                            2360.0953252379227, 
                            805.6778364977225, 
                            -725.1938418055298, 
                            0.8350182225972514, 
                            2.8083181848844427, 
                            -1.1329671981512124
                        ], 
                        ...
                    ], 
                }, 
                "EME2000": {
                    "position": [
                        1928870.0889872166, 
                        -1288165.3512322104, 
                        6748298.746048956
                    ], 
                    "velocity": [
                        -7103.215338163427, 
                        799.0277755905057, 
                        2178.269986868109
                    ],
                    "covarianceExtended": [...],
                    "covariance": [...]
                }
            }, 
            "coefficients": {
                "fitted": {
                    "drag": 0.012670258477322949, 
                    "reflectivity": 0.034625933368881534
                }
            }
        }
    ]
}
```

Ephemeris Propagation
(using the 'id' and 'timestamp' from list-states, propagation up to +/- 7 days is supported)
```
leolabs catalog get-propagation --catalog-number L335 --state 411615 --start-time "2017-11-08T00:00:00Z" --end-time "2017-11-08T00:10:00Z" --timestep 60
{
    "state": "411615", 
    "startTime": "2017-11-08T00:00:00+00:00", 
    "endTime": "2017-11-08T00:10:00+00:00"
    "timestep": 60.0, 
    "frame": "EME2000", 
    "propagation": [
        {
            "position": [
                3332379.5, 
                389069.125, 
                -6315865.0
            ], 
            "covariance": [
                [
                    29974.513671875, 
                    -24190.095703125, 
                    2371.23681640625
                ], 
                [
                    -24190.095703125, 
                    37943.2265625, 
                    3726.4931640625
                ], 
                [
                    2371.23681640625, 
                    3726.4931640625, 
                    2056.061279296875
                ]
            ], 
            "velocity": [
                6493.70166015625, 
                -1525.608154296875, 
                3333.548828125
            ]
        }, 
        ...
    ], 
}
```
