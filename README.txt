top mod list
regex

don't clear white space if md
paste remap
context plugin

---------------------

fly.io
write testing 
dev branch

-------------------------------------------------------

WRITE MOD TOP LIST COMMAND

when a user bans / kicks / mutes an other (unique) user, then they get 1 mod score
this should count the actions done by the mod and the actions done through the bot too
the actions should be requested from audit logs
options for filtering: page, action type, months

SHOULD count a user's manual ban & bot ban

page: int
action type: (require) kick, mute, ban
months: int

------------- ------------- ------------- -------------

def mod_top_list(page=None, action_type=None, n_months=None):
    data = REQUEST data from audit log from x months
    mod_score = {}
    
    loop through the data
        check if (action_type is not the specified one) and (the action type is not all)
            continue

        try:
            add 1 to user score in mod_score
        except
            add user to mod_score with score 1

        add to mod score
    
    paginate the output
    send the page
