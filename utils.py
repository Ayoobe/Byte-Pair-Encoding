def stats(text):
    counts = {}
    for pair in zip(text, text[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def merge(text,pair,rep):
  i=0
  new_text=[]
  while i <len(text) :
    if  i <len(text) - 1 and text[i]==pair[0] and text[i+1]==pair[1]:
      new_text.append(rep)
      i+=2
    else:
      new_text.append(text[i])
      i+=1
  return new_text


