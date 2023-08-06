friends_template = '''var user = {user_id};
                      var i = 0;
                      var ret = [];
                      var count = {count};
                      var data = {{ }};
                      while (i*1000 < count)
                      {{
                          data = API.friends.get({{"user_id":user, "count":1000, "offset":i*1000}});
                          count = data["count"];
                          ret.push(data["items"]);
                          i=i+1;
                      }}
                      return {{"count":count, "items":ret}};'''

subs_25k_template = '''var user = {user_id};
                       var i = 0;
                       var ret = [];
                       var count = 25000;
                       var data = {{ }};
                       while (i*1000 < count &&  i<25)
                       {{
                           data = API.users.getFollowers({{"user_id":user,
                           "count":1000, "offset":i*1000 + {offset} }});
                           count = data["count"];
                           ret.push(data["items"]);
                           i=i+1;
                       }}
                       return {{"count":count, "items":ret}};'''


videos_5k_template = '''var user = {user_id};
               var i = 0;
               var ret = [];
               var count = 5000;
               var data = {{ }};
               while (i*200 < count &&  i<25)
               {{
                   data = API.video.get({{"user_id":user, 
                   "count":200, "offset":i*200}});
                   count = data["count"];
                   ret.push(data["items"]);
                   i=i+1;
               }}
               return {{"count":count, "items":ret}};'''


members_25k_template = '''var group = "{}";
                                var i = 0;
                                var count = 25000;
                                var ret = {{ }};
                                var data = {{ }};
                                while (i < 25 && i*1000 < count)
                                {{
                                    data = API.groups.getMembers({{"group_id":group, "count":1000,
                                     "offset":i*1000 + {}, "fields":"{}"}});
                                    count = data["count"];
                                    ret.push(data["items"]);
                                    i=i+1;
                                }}
                                return {{"count":count, "items":ret}};'''


groups_25_members_template = '''var groups = {};
                                var i = 0;
                                var ret = {{}};
                                while (i < 25 && i < groups.length)
                                {{
                                    ret.push({{"id":groups[i], "response":API.groups.getMembers(
                                    {{"group_id":groups[i], "count":1000, "fields":"{}"}})}});
                                    i=i+1;
                                }}
                                return ret;'''


users_25_subscriptions_template = '''var ids = [{ids}];
                                     var i = 0;
                                     var ret = {{ }};
                                     while (i < 25 && i < ids.length)
                                     {{
                                         ret.push({{"id":ids[i], "response":API.users.getSubscriptions({{"user_id":ids[i], 
                                         "extended":0, "count":200}})}});
                                         i=i+1;
                                     }}
                                     return ret;'''


users_25_groups_template = '''var ids = [{ids}];
                              var i = 0;
                              var ret = {{ }};
                              while (i < 25 && i < ids.length)
                              {{
                                  ret.push({{"id":ids[i], "response":API.groups.get({{"user_id":ids[i], 
                                  "extended":1, "count":500}})}});
                                  i=i+1;
                              }}
                              return ret;'''


users_25_friends_template = '''var ids = [{ids}];
                               var i = 0;
                               var ret = {{}};
                               while (i < 25 && i < ids.length)
                               {{
                                   ret.push({{"id":ids[i], "response":API.friends.get({{"user_id":ids[i], 
                                   "count":1000}})}});
                                   i=i+1;
                               }}
                               return ret;'''


users_25_subs_template = '''var ids = [{ids}];
                            var i = 0;
                            var ret = {{ }};
                            while (i < 25 && i < ids.length)
                            {{
                                ret.push({{"id":ids[i], 
                                "response":API.users.getFollowers({{"user_id":ids[i], "count":1000}})}});
                                i=i+1;
                            }}
                            return ret;'''


users_25_videos_template = '''var ids = [{ids}];
                              var i = 0;
                              var ret = {{ }};
                              while (i < 25 && i < ids.length)
                              {{
                                  ret.push({{"id":ids[i], 
                                  "response":API.video.get({{"owner_id":ids[i], "count":200}})}});
                                  i=i+1;
                              }}
                              return ret;'''


def join_execute_response(resp):
    if resp['response']['count'] is None:
        return []
    return [i for array in resp['response']['items'] for i in array]
