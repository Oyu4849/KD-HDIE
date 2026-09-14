from datasource.connectors.csv_connector import CSVConnector

connector = CSVConnector(
    file_path="media/aral_monthly_heterogeneous_2017_2025.csv"
)

result = connector.read()

print("=" * 60)

print("SUCCESS :", result.success)

print("ROWS    :", len(result.data))

print("COLUMNS :", result.metadata["columns"])

print()

print("FIRST RECORD")

print(result.data[0])

print("=" * 60)
