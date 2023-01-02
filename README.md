# IPX10G Port Bandwidth and Status Collector

The purpose of this script module is to collect port status and bandwidth information from the 3080IPX-10G card family. The poller script uses the cfgjsonrpc webeasy program to gather information.

The data collection module has the below distinct abilities and features:

1. Collects RX and TX Rate
2. Collects Port Operational Status

## Minimum Requirements:

-   inSITE Version 10.3 and service pack 6
-   Python3.7 (_already installed on inSITE machine_)
-   Python3 Requests library (_already installed on inSITE machine_)

## Installation:

Installation of the status monitoring module requires copying two scripts into the poller modules folder:

1. Copy **ipx_port_collector.py** script to the poller python modules folder:

    ```
     cp scripts/ipx_port_collector.py /opt/evertz/insite/parasite/applications/pll-1/data/python/modules
    ```

2. Restart the poller application

## Configuration:

To configure a poller to use the module start a new python poller configuration outlined below

1. Click the create a custom poller from the poller application settings page
2. Enter a Name, Summary and Description information
3. Enter the host value in the _Hosts_ tab
4. From the _Input_ tab change the _Type_ to **Python**
5. From the _Input_ tab change the _Metric Set Name_ field to **ipx**
6. Select the _Script_ tab, then paste the contents of **scripts/poller_config.py** into the script panel.
7. Save changes, then restart the poller program.

## Sample Output

```
{
    "l_input_rate": 140773000,
        "as_id": [
        "32.0@i",
        "33.0@i",
        "306.0@s",
        "252.0@i",
        "303.0@s"
    ],
    "i_port": 1,
    "l_output_rate": 0,
    "s_label": "10G/1G SFP+ Port (xeth1)",
    "s_operation_status": "UP",
    "s_name": "1"
}

```
