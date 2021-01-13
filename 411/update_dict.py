import pickle

with open('url_cotent_vps.txt', 'rb') as f:
    content_state_vps = pickle.load(f)

with open('url_cotent.txt', 'rb') as f:
    content_state = pickle.load(f)

content_state.update(content_state_vps)

with open('url_cotent.txt', 'wb') as f:
    pickle.dump(content_state, f)
