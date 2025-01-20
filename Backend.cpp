#include <mavsdk/mavsdk.h>
#include <mavsdk/plugins/mavlink_passthrough/mavlink_passthrough.h>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>
#include <thread>
#include <cmath>
#include <vector>
#include <mutex>
#include <fstream> // For file handling

using namespace mavsdk;
using namespace std;

void usage(const string &bin_name)
{
    cerr << "Usage : " << bin_name << " <connection_url>\n"
         << "Connection URL format should be:\n"
         << "  For UDP  : udp://[bind_host][:bind_port]\n"
         << "  For TCP  : tcp://[server_host][:server_port]\n"
         << "  For Serial: serial:///path/to/serial/dev[:baudrate]\n"
         << "Example: udp://:14540\n";
}

int main()
{
    Mavsdk mavsdk{Mavsdk::Configuration{1, MAV_COMP_ID_ONBOARD_COMPUTER, false}};
    const string connection_url = "udp://192.168.144.12:19856";

    const ConnectionResult connection_result = mavsdk.add_any_connection(connection_url);

    if (connection_result != ConnectionResult::Success)
    {
        cerr << "Connection failed: " << connection_result << endl;
        return 1;
    }

    shared_ptr<System> system = nullptr;
    cout << "Waiting for system to connect...\n";

    for (int i = 0; i < 30; ++i)
    {
        if (!mavsdk.systems().empty())
        {
            system = mavsdk.systems().at(0);
            break;
        }
        cout << "Attempt " << i + 1 << ": No system detected yet.\n";
        this_thread::sleep_for(chrono::seconds(1));
    }

    if (!system)
    {
        cerr << "Timed out waiting for a system to connect.\n";
        return 1;
    }

    cout << "System connected, System ID: " << system->get_system_id() << endl;

    auto mavlink_passthrough = MavlinkPassthrough{system};

    double roll_deg = 0.0;
    double pitch_deg = 0.0;
    double yaw_deg = 0.0;
    vector<double> battery_voltages(10, -1.0);
    double latitude_deg = 0.0;
    double longitude_deg = 0.0;
    double altitude_m = 0.0;

    mutex data_mutex;

    mavlink_passthrough.subscribe_message(
        MAVLINK_MSG_ID_ATTITUDE,
        [&roll_deg, &pitch_deg, &yaw_deg, &data_mutex](const mavlink_message_t &message)
        {
            mavlink_attitude_t attitude;
            mavlink_msg_attitude_decode(&message, &attitude);

            lock_guard<mutex> lock(data_mutex);
            roll_deg = attitude.roll * 180.0 / M_PI;
            pitch_deg = attitude.pitch * 180.0 / M_PI;
            yaw_deg = attitude.yaw * 180.0 / M_PI;
        });

    mavlink_passthrough.subscribe_message(
        MAVLINK_MSG_ID_BATTERY_STATUS,
        [&battery_voltages, &data_mutex](const mavlink_message_t &message)
        {
            mavlink_battery_status_t battery_status;
            mavlink_msg_battery_status_decode(&message, &battery_status);

            lock_guard<mutex> lock(data_mutex);
            for (int i = 0; i < 10; ++i)
            {
                if (battery_status.voltages[i] != std::numeric_limits<uint16_t>::max())
                {
                    battery_voltages[i] = battery_status.voltages[i] / 1000.0; // Convert mV to V
                }
            }
        });

    mavlink_passthrough.subscribe_message(
        MAVLINK_MSG_ID_GLOBAL_POSITION_INT,
        [&latitude_deg, &longitude_deg, &altitude_m, &data_mutex](const mavlink_message_t &message)
        {
            mavlink_global_position_int_t global_position;
            mavlink_msg_global_position_int_decode(&message, &global_position);

            lock_guard<mutex> lock(data_mutex);
            latitude_deg = global_position.lat / 1e7;
            longitude_deg = global_position.lon / 1e7;
            altitude_m = global_position.alt / 1000.0;
        });

    // Create and open an output file
    ofstream output_file("output.txt");
    ofstream Altitude("Altitude.txt");
    ofstream pitch("Pitch.txt");
    ofstream yaw("yaw.txt");
    ofstream roll("roll.txt");
    ofstream gps("gps.txt");

    if (!output_file.is_open())
    {
        cerr << "Failed to open output file.\n";
        return 1;
    }

    cout << "Listening for attitude, battery, and GPS data... ";

    while (true)
    {
        {
            lock_guard<mutex> lock(data_mutex);
            double total_voltage = 0;

        auto now = chrono::system_clock::now();
        auto time_since_epoch = now.time_since_epoch();
        auto seconds = chrono::duration_cast<std::chrono::seconds>(time_since_epoch).count();

\
        time_t current_time = std::chrono::system_clock::to_time_t(now);
        stringstream time_stream;
        time_stream << std::put_time(std::localtime(&current_time), "%Y-%m-%d %H:%M:%S");

        string timestamp = time_stream.str() + " ";  // Format the timestamp

            // // Clear the console for next update (optional)
            // cout << "\033[2J\033[H";

            // // Write to the file
            // output_file << "Pitch: " << pitch_deg << "°\n";
            // output_file << "Roll: " << roll_deg << "°\n";
            // output_file << "Yaw: " << yaw_deg << "°\n";

            // output_file << "Battery Voltages: ";
            // for (double voltage : battery_voltages) {
            //     if (voltage >= 0.0) {
            //         output_file << voltage << " V ";
            //         total_voltage += voltage;
            //     }
            // }
            // output_file << "\n";
            // output_file << "Total Battery Voltage: " << total_voltage << "\n";
            // output_file << "\n";
            // output_file << "GPS Coordinates: \n";
            // output_file << "  Latitude: " << latitude_deg << "°\n";
            // output_file << "  Longitude: " << longitude_deg << "°\n";
            // output_file << "  Altitude: " << altitude_m << " m\n";
            // Optionally flush the buffer after each write to ensure data is written to the file immediately

            // Write to the file in x|y|z|... format
       
            output_file << pitch_deg << "|"
                        << roll_deg << "|"
                        << yaw_deg << "|";

            for (double voltage : battery_voltages)
            {
                if (voltage >= 0.0)
                {
                    output_file << voltage << "|";
                    total_voltage += voltage;
                }
            }

            output_file << total_voltage << "|"
                        << latitude_deg << "|"
                        << longitude_deg << "|"
                        << altitude_m << "|\n";

                        //totalvolts| latitude_de
                        

            output_file.flush();

            pitch << timestamp <<  altitude_m;
            yaw << timestamp <<  yaw_deg;
            roll << timestamp <<  roll_deg;
            gps << timestamp << latitude_deg << "," << longitude_deg;
        }
        this_thread::sleep_for(chrono::milliseconds(500)); // Adjust sleep time as needed
    }

    output_file.close(); // Close the file when done

    return 0;
}
