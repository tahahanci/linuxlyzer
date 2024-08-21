import json
from network_check import network_check
from process_check import process_check
from directory_check import directory_check
from file_check import file_check
from user_check import user_check
from log_check import log_check


def format_output(data):
    formatted_output = json.dumps(data, indent=4)
    return formatted_output


def save_output(data, output_format='json'):
    formatted_data = format_output(data)

    with open('output.json', 'w') as f:
        f.write(formatted_data)

    if output_format == 'txt':
        with open('output.txt', 'w') as f:
            f.write(formatted_data)


if __name__ == "__main__":
    choice = input(
        "Hangi kontrolü çalıştırmak istersiniz? (network, processes, directories, files, users, logs, all): ").strip().lower()
    output_format = input("Çıktı formatı ne olsun? (json, txt, terminal): ").strip().lower()

    if choice == "network":
        network_data = network_check()
        save_output(network_data, output_format)
    elif choice == "processes":
        process_data = process_check()
        save_output(process_data, output_format)
    elif choice == "directories":
        directory_data = directory_check()
        save_output(directory_data, output_format)
    elif choice == "files":
        file_data = file_check()
        save_output(file_data, output_format)
    elif choice == "users":
        user_data = user_check()
        save_output(user_data, output_format)
    elif choice == "logs":
        log_data = log_check()
        save_output(log_data, output_format)
    elif choice == "all":
        network_data = network_check()
        process_data = process_check()
        directory_data = directory_check()
        file_data = file_check()
        user_data = user_check()
        log_data = log_check()
        all_data = {
            "network": network_data,
            "processes": process_data,
            "directories": directory_data,
            "files": file_data,
            "users": user_data,
            "logs": log_data
        }
        save_output(all_data, output_format)
    else:
        print("Geçersiz seçim. Lütfen 'network', 'processes', 'directories', 'files', 'users', 'logs' veya 'all' seçeneklerinden birini seçin.")