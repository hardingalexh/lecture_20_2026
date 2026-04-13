import requests
import matplotlib.pyplot as plt
import time


def get_hospitalization_data():
    hospitalizations_url = (
        "https://data.cdc.gov/resource/aemt-mg7g.json?jurisdiction=NC"
    )
    hosp_file = requests.get(hospitalizations_url)
    hosp_file = hosp_file.json()
    output = []
    last_number = 0
    for row in hosp_file:
        admissions = int(row.get("total_admissions_all_covid_confirmed"))
        new_row = {
            "week_end_date": row.get("week_end_date"),
            "hospitalizations": last_number + admissions,
        }
        last_number += admissions
        output.append(new_row)
    return output


def get_vaccination_data():
    vaccinations_url = "https://data.cdc.gov/resource/unsk-b7fc.json?location=NC"
    vacc_file = requests.get(vaccinations_url)
    vacc_file = vacc_file.json()
    output = []
    for row in vacc_file:
        new_row = {"date": row.get("date"), "vaccinations": row.get("administered")}
        output.append(new_row)
    return output


def harmonize(vacc_data, hosp_data):
    output = []
    for row in hosp_data:

        def match_dates(x):
            return x.get("date") == row.get("week_end_date")

        matching_vacc_rows = list(filter(match_dates, vacc_data))

        if len(matching_vacc_rows):
            row["vaccinations"] = matching_vacc_rows[0].get("vaccinations")
            output.append(row)
    return output


def visualize(harmonized):
    fig, axs = plt.subplots(2, 1, layout="constrained")
    dates = [d.get("week_end_date") for d in harmonized]
    vacc = [d.get("vaccinations") for d in harmonized]
    hosp = [d.get("hospitalizations") for d in harmonized]
    axs[0].plot(dates, vacc)
    axs[1].plot(dates, hosp)
    # axs[0].plot(t, s1, t, s2)
    # axs[0].set_xlim(0, 2)
    # axs[0].set_xlabel('Time (s)')
    # axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    # cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
    # axs[1].set_ylabel('Coherence')

    plt.show()


def main():
    start = time.time()
    hosp_data = get_hospitalization_data()
    vacc_data = get_vaccination_data()
    harmonized = harmonize(vacc_data, hosp_data)
    # visualize(harmonized)
    print(time.time() - start)


main()

# output = []
# for row in vacc_file.json():
#     output.append(row.get("end_date"))
