import requests
import json

# AppSync API information
url = "https://zbb272wkr5au7littrgcwsvafq.appsync-api.eu-west-2.amazonaws.com/graphql"
bearer_token = "Bearer eyJhbGciOiJSUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzLUJqMGJDcEhqakJnTGhuUFE1cldENmF6SkNNOVFSUGxYX05OcVNSRGpJIn0.eyJleHAiOjE3NjMwMjEzNjEsImlhdCI6MTc0NzQ2OTM2MSwianRpIjoiZTQ5NzVmYTEtMjYyMy00NmZiLWFmODAtYTYxMmFkMmI4ZjM1IiwiaXNzIjoiaHR0cHM6Ly9kZXYtaWQuYmxpbmsuZ2xvYmFsL3JlYWxtcy9ibGluay1pZCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIwYmQ2MDA5Ni1lZmRhLTQ1OWUtYmJiYy0yYThjZDMzMmIwNGIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJub2l0cy1hY2Nlc3MiLCJzaWQiOiJlNWVlYTRmYy1kZTk5LTQ5MTYtYTZiNy1lZTczNmY1MzI5YWUiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZGV2LXNob3AuYmxpbmsuZ2xvYmFsLyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtYmxpbmsgaWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJkZWxldGUtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgY29nbml0bzpncm91cHMgY3VzdG9tLWF1dGgiLCJjb2duaXRvOmdyb3VwcyI6ImFkbWluIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF1dGhfdGltZSI6MTc0NzQ2OTM2MSwibmFtZSI6Im1hbWhvdWQgYW1wbGlmeXVzZXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtYWhtb3VkK2FtcGxpZnlkZXZAYmxpbmsuZ2xvYmFsIiwiZ2l2ZW5fbmFtZSI6Im1hbWhvdWQiLCJmYW1pbHlfbmFtZSI6ImFtcGxpZnl1c2VyIiwiZW1haWwiOiJtYWhtb3VkK2FtcGxpZnlkZXZAYmxpbmsuZ2xvYmFsIn0.MrXCS6G4hgy2E7JU8I_4aI6MzJI4Yge0MxdDibqZNdVTbh0vigTtaJDeAaF2Cn39rv9DvJTo2bnOO8X05_K6IvkPeWfkXfl9V68IbhZ3Dt29Bc0j-oD_pf6uzY6mvH6ZmztpaxNkaKaRR0WGOpvTSxIbcUzrVGSZWG9XV2ULRRYMV40UDcGTWbENySl79iC8Ec3GsEOp3pPe_3K2v5BUHTMeM2lCUbH9ou2rdJVNsC9zmlgyVGPzXKyG2QpjOaViq-Uy8bovyz-77yyYdnKUtJg5SbwW_nzrUqT6FaQeKAd7c4T8-ytWaDjfQTpUi5syHgnUFXEB2LbC6kTxbW7jJA"

# Configure headers for AppSync API with Bearer token (like Postman)
headers_bearer = {
    "Content-Type": "application/json",
    "Authorization": bearer_token
}

# Simple GraphQL query
query = {
    "query": "query SyncCategories { syncCategories(limit: 10) {nextToken items {id name} } }"
}

print("Sending request to AppSync API with Bearer token only (like Postman)...")
print(f"URL: {url}")
print(f"Headers: {json.dumps(headers_bearer, indent=2)}")
print(f"Query: {json.dumps(query, indent=2)}")

# Make the API request
try:
    response = requests.post(url, json=query, headers=headers_bearer)
    
    print("\nResponse Details:")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {json.dumps(dict(response.headers), indent=2)}")
    
    if response.status_code >= 400:
        print(f"Error Response: {response.text}")
    else:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        
except Exception as e:
    print(f"Exception occurred: {str(e)}") 