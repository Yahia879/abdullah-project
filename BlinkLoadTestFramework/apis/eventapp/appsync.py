import json
import time
import random
from datetime import datetime, timedelta
from apis import base_api

# Static variables
url = "https://zbb272wkr5au7littrgcwsvafq.appsync-api.eu-west-2.amazonaws.com/graphql"
token = "Bearer eyJhbGciOiJSUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzLUJqMGJDcEhqakJnTGhuUFE1cldENmF6SkNNOVFSUGxYX05OcVNSRGpJIn0.eyJleHAiOjE3NjMwMjEzNjEsImlhdCI6MTc0NzQ2OTM2MSwianRpIjoiZTQ5NzVmYTEtMjYyMy00NmZiLWFmODAtYTYxMmFkMmI4ZjM1IiwiaXNzIjoiaHR0cHM6Ly9kZXYtaWQuYmxpbmsuZ2xvYmFsL3JlYWxtcy9ibGluay1pZCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIwYmQ2MDA5Ni1lZmRhLTQ1OWUtYmJiYy0yYThjZDMzMmIwNGIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJub2l0cy1hY2Nlc3MiLCJzaWQiOiJlNWVlYTRmYy1kZTk5LTQ5MTYtYTZiNy1lZTczNmY1MzI5YWUiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZGV2LXNob3AuYmxpbmsuZ2xvYmFsLyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtYmxpbmsgaWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJkZWxldGUtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgY29nbml0bzpncm91cHMgY3VzdG9tLWF1dGgiLCJjb2duaXRvOmdyb3VwcyI6ImFkbWluIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF1dGhfdGltZSI6MTc0NzQ2OTM2MSwibmFtZSI6Im1hbWhvdWQgYW1wbGlmeXVzZXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtYWhtb3VkK2FtcGxpZnlkZXZAYmxpbmsuZ2xvYmFsIiwiZ2l2ZW5fbmFtZSI6Im1hbWhvdWQiLCJmYW1pbHlfbmFtZSI6ImFtcGxpZnl1c2VyIiwiZW1haWwiOiJtYWhtb3VkK2FtcGxpZnlkZXZAYmxpbmsuZ2xvYmFsIn0.MrXCS6G4hgy2E7JU8I_4aI6MzJI4Yge0MxdDibqZNdVTbh0vigTtaJDeAaF2Cn39rv9DvJTo2bnOO8X05_K6IvkPeWfkXfl9V68IbhZ3Dt29Bc0j-oD_pf6uzY6mvH6ZmztpaxNkaKaRR0WGOpvTSxIbcUzrVGSZWG9XV2ULRRYMV40UDcGTWbENySl79iC8Ec3GsEOp3pPe_3K2v5BUHTMeM2lCUbH9ou2rdJVNsC9zmlgyVGPzXKyG2QpjOaViq-Uy8bovyz-77yyYdnKUtJg5SbwW_nzrUqT6FaQeKAd7c4T8-ytWaDjfQTpUi5syHgnUFXEB2LbC6kTxbW7jJA"

def get_last_sync_timestamp():
    now = datetime.now()
    
    five_days_ago = now - timedelta(days=5)
    
    now_timestamp = now.timestamp()
    days_ago_timestamp = five_days_ago.timestamp()
    
    
    random_timestamp = random.uniform(days_ago_timestamp, now_timestamp)
    
    
    return int(random_timestamp * 1000)


categories_template = "query SyncCategories {{ syncCategories(lastSync: {}, limit: 1200) {{nextToken items {{id name _deleted _lastChangedAt _version bgColorDark bgColorLight bgColorToken createdAt eventIds fgColorDark fgColorLight fgColorToken iconCode isFeatured isSearchable largeImage  order parentCategoryId thumbImage type updatedAt }} }} }}"

entities_template = "query syncEntities {{ syncEntities(lastSync: {}, limit: 1200) {{nextToken items {{id name _deleted _lastChangedAt _version bgColorDark bgColorLight bgColorToken createdAt eventIds fgColorDark fgColorLight fgColorToken iconCode isFeatured isSearchable largeImage  order parentCategoryId thumbImage type updatedAt }} }} }}"

places_template = "query SyncPlaces {{ syncPlaces(lastSync: {}, limit: 5000) {{ items {{ _deleted _lastChangedAt _version about address category coverImage createdAt eventIds id image latitude longitude name operationHours order phone pricing rating typeId updatedAt }} }} }}"

halls_template = "query SyncHalls {{ syncHalls(lastSync: {}, limit: 5000) {{nextToken items {{id name _deleted _lastChangedAt _version accessibilityChecklist capacity createdAt description details direction eventIds gallery image links order over18Venue isPublished updatedAt venueId }}}}}}"

venues_template = "query SyncVenues {{ syncVenues(lastSync: {}, limit: 5000, nextToken:null) {{ nextToken items {{ id name _deleted _lastChangedAt _version accessibilityChecklist address operationHours capacity city country createdAt description eventIds gallery image isFeatured isPublished latitude links longitude navigationUrl order over18Venue province street subtitle updatedAt zip }} }} }}"

sessions_template = "query SyncSessions {{ syncSessions(lastSync: {}, limit: 5000 ) {{ nextToken items {{id title _deleted _lastChangedAt _version addedToScheduleCount capacityId  createdAt description startDate endDate endTimeInMinutes  eventIds hallId isCanceled isDeleted isFeatured isHidden isLocked isPublished isTrending landscapeImage order pollUrl portraitImage squareImage  startTimeInMinutes subtitle updatedAt urls venueId accessibilityChecklist childIdRefs entityIdRefs childEntityIdRefs categoryIdRefs primaryEntityCategoryIdRefs primaryCategoryId}}  }}}}"

def set_url(new_url):
    global url
    url = new_url

def set_token(new_token):
    global token
    token = new_token

def get_endpoint():
    return url

def get_method():
    return "POST"

def get_headers():
    return base_api.appsync_headers


def create_categories_message():
    timestamp = get_last_sync_timestamp()
    query = categories_template.format(timestamp)
    return json.dumps({"query": query})

def create_entities_message():
    timestamp = get_last_sync_timestamp()
    query = entities_template.format(timestamp)
    return json.dumps({"query": query})

def create_places_message():
    timestamp = get_last_sync_timestamp()
    query = places_template.format(timestamp)
    return json.dumps({"query": query})

def create_halls_message():
    timestamp = get_last_sync_timestamp()
    query = halls_template.format(timestamp)
    return json.dumps({"query": query})

def create_venues_message():
    timestamp = get_last_sync_timestamp()
    query = venues_template.format(timestamp)
    return json.dumps({"query": query})

def create_sessions_message():
    timestamp = get_last_sync_timestamp()
    query = sessions_template.format(timestamp)
    return json.dumps({"query": query}) 