
from sleepmusicalization import controller


def main():
    analysis_result_json_string = open("json_export_sample/sample_analysis_result.json").read()
    sleep_result_json_string = open("json_export_sample/sample_sleep_result.json").read()
    
    controller.composeSong(analysis_result_json_string, sleep_result_json_string)

if __name__ == "__main__":
    main()
