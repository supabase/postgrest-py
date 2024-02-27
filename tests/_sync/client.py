from postgrest import SyncPostgrestClient

REST_URL = "https://kzwoknoxuuvryajohvij.supabase.co/rest/v1/"
headers = {}
headers[
    "apikey"
] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6d29rbm94dXV2cnlham9odmlqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgxOTAxNzgsImV4cCI6MjAyMzc2NjE3OH0.Nz3iqSWRryPmvLpCTb-6tyMe5X4I8NATQmy9xfr13l0"
headers[
    "Authorization"
] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6d29rbm94dXV2cnlham9odmlqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgxOTAxNzgsImV4cCI6MjAyMzc2NjE3OH0.Nz3iqSWRryPmvLpCTb-6tyMe5X4I8NATQmy9xfr13l0"


def rest_client():
    return SyncPostgrestClient(base_url=REST_URL, headers=headers)
