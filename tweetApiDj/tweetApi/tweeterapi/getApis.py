import os
import requests

END_POINTS={
    "get_user_id":lambda x:f"users/by/username/{x}", # :username
    "get_user_tweets": lambda x:f"users/{x}/tweets",
    "get_complete_tweet": lambda x:f"tweets/{x}"
}

def create_url(endpoint:str):
    url = f"https://api.twitter.com/2/{endpoint}"
   
    return url


# users/by/username/{username}

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers,params=None):
     #params object received from create_url function
    response = requests.get(url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# response.json()["data"]["id"]
# if __name__=="__main__":
#     print("..............................GET USER ID............\n................................")
    
#     bearer_token ="AAAAAAAAAAAAAAAAAAAAAIywegEAAAAAMGXRW7jCsPmkRRgrXOLtvL%2BIc1s%3DveLtNNmzLD6Gt6xudSd97AVnHFXb7eb6PJZlS0Et7KpVgkXBXh"
#     url = create_url(END_POINTS["get_user_id"]("DarrellMello"))
#     # url = create_url(END_POINTS["get_user_id"]("DarrellMello"))
#     headers = create_headers(bearer_token)
#     json_response = connect_to_endpoint(url, headers)
#     print(json_response)
#     print("...............................Get USER TWEETS...........\n................................")
    
#     url=create_url(END_POINTS["get_user_tweets"](json_response["data"]["id"]))
#     json_response = connect_to_endpoint(url, headers,{
#         "expansions":"author_id,referenced_tweets.id.author_id",
#         "max_results":5,
#         "tweet.fields":"created_at,author_id,id,text",
#         "user.fields":"profile_image_url",
#         "media.fields":"url"
#     })
    
#     print(json_response)
#     print("........................")
#     user_name=""
#     profile_image_url=""
#     for user in json_response["includes"]["users"]:
#         if user["id"]==json_response["includes"]["tweets"][0]["author_id"]:
#             user_name=user["username"]
#             profile_image_url=f"<img src=\"{user['profile_image_url']}\" alt=\"{user_name}\">"
#     res ={
#         "recent_tweet":json_response["includes"]["tweets"][0]['text'],
#         "twitter_handle":user_name,
#         "created_at":json_response["data"][0]["created_at"],
#         "link":f"<a href=\"{f'https://twitter.com/{user_name}'}\">@{user_name}</a>",
#         "text":json_response["includes"]["tweets"][0]["text"],
#         "profile_image_url":profile_image_url
#     }
#     print(res)
#     print("..........................................\n................................")
    

    # url=create_url(END_POINTS["get_complete_tweet"](json_response["data"][0]["id"]))
    # json_response = connect_to_endpoint(url, headers)
    
    # "https://pbs.twimg.com/profile_images/1409530084030025732/fMdEhpIb_400x400.jpg"
    # res ={
    #      imgHtml:,
    #     timeHtml:time,
    #     contentHtml:str(content),
    #     href:href,
    #     tweetedByHtml:tweetedBy 
    # }
    # print(json_response)

class Tweet:
    def __init__(self,imgHtml:str,timeHtml:str,contentHtml:str,tweetedByHtml:str,href:str):
        self.imgHtml = imgHtml
        self.timeHtml = timeHtml
        self.contentHtml = contentHtml
        self.tweetedByHtml = tweetedByHtml
        self.href = href
        
    def to_json(self):
        return {
            "imgHtml":self.imgHtml,
            "timeHtml":self.timeHtml,
            "href":self.href,
            "contentHtml":self.contentHtml,
            "tweetedByHtml":self.tweetedByHtml 
        }

def getRecentTweets(twitterHandle: str):
    print("..............................GET USER ID............\n................................")
    
    bearer_token = os.getenv("BEARER_TOKEN")
    url = create_url(END_POINTS["get_user_id"](twitterHandle))
    # url = create_url(END_POINTS["get_user_id"]("DarrellMello"))
    headers = create_headers(bearer_token)
    try:
        json_response = connect_to_endpoint(url, headers)
        print(json_response)
        print("...............................Get USER TWEETS...........\n................................")
        url=create_url(END_POINTS["get_user_tweets"](json_response["data"]["id"]))
        json_response = connect_to_endpoint(url, headers,{
        "expansions":"author_id,referenced_tweets.id.author_id",
        "max_results":5,
        "tweet.fields":"created_at,author_id,id,text",
        "user.fields":"profile_image_url",
        "media.fields":"url"
            })
    
        print(json_response)
        print("........................")
        user_name=""
        profile_image_url=""
        for user in json_response["includes"]["users"]:
            if user["id"]==json_response["includes"]["tweets"][0]["author_id"]:
                user_name=user["username"]
                profile_image_url=f"{user['profile_image_url']}"
        res ={
            "recent_tweet":json_response["includes"]["tweets"][0]['text'],
            "twitter_handle":user_name,
            "created_at":json_response["data"][0]["created_at"],
            "link":{f'https://twitter.com/{user_name}'},
        "text":json_response["includes"]["tweets"][0]["text"],
        "profile_image_url":profile_image_url
    }    
        img = res["profile_image_url"]
        time =res["created_at"]
        content = res['text']
        tweetedBy=res["twitter_handle"]
        href=res["link"]
        res = Tweet(
            imgHtml=img,
            timeHtml=time,
            contentHtml=content,
            href=href,
            tweetedByHtml=tweetedBy 
        )
    

        return res.to_json()

    except Exception as e:
   
        print("Something went wrong")
        print(e)
   
        return {}



if __name__=="__main__":
    s=getRecentTweets("DarrellMello")
    print("/**************************/")
    print(s)
    print("/***************************/")

    s=getRecentTweets("GVDBossche")
    print("/***************************/")
    print(s)
    print("/***************************/")
