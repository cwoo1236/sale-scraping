import re
from scrape_arket_sale import scrape_arket_sale

# TODO: 
# "english mode" when searching?: black AND pants FROM arket UNDER 50 OR blue AND shorts FROM abercrombie

def tokenize(input):
  if not input:
    return []
  if re.match('"([\w ]+)"', input):
    tok = re.match('"([\w ]+)"', input).group(1)
    return [('ID', tok)] + tokenize(input[len(tok):])
  elif re.match("&", input):
    return ['AND'] + tokenize(input[1:])
  elif re.match("\|", input):
    return ['OR'] + tokenize(input[1:])
  elif re.match("<(\d+)", input):    # e.g. <50
    tok = re.match("<(\d+)", input).group(1)
    return [('UNDER', tok)] + tokenize(input[len(tok) + 1:])
  elif re.match(">(\d+)", input):    # e.g. >25
    tok = re.match(">(\d+)", input).group(1)
    return [('OVER', tok)] + tokenize(input[len(tok) + 1:])
  elif re.match(':(\w+)', input):
    tok = re.match(':(\w+)', input).group(1)
    return [('FROM', tok)] + tokenize(input[len(tok) + 1:])
  elif re.match('\*', input):
    return [('WC', 'all')] + tokenize(input[1:])
  elif re.match('(\w+)', input):
    tok = re.match('(\w+)', input).group(0)
    return [('ID', tok)] + tokenize(input[len(tok):])
  elif re.match('\s', input):
    return tokenize(input[1:])
  else:
    raise SyntaxError("Invalid token found in search term")


# PARSE
def parse_or(tokens):
  (t, left) = parse_unary(tokens)
  if t and t[0] == 'OR':
    (tt, right) = parse_or(t[1:])
    return (tt, ('OR', left, right))
  else:
    return (t, left)

def parse_unary(tokens):
  if tokens and (tokens[0][0] == 'FROM' or tokens[0][0] == 'OVER' or tokens[0][0] == 'UNDER'):
    tok_type = tokens[0][0]
    val = tokens[0][1]
    (t, res) = parse_unary(tokens[1:])
    return (t, (tok_type, val, res))
  else:
    return parse_and(tokens)

def parse_and(tokens):
  (t, left) = parse_id(tokens)
  if t and t[0] == 'AND':
    (tt, right) = parse_and(t[1:])
    return (tt, ('AND', left, right))
  else:
    return (t, left)


def parse_id(tokens):
  if tokens:
    return (tokens[1:], tokens[0])
  else:
    raise SyntaxError("Unexpected end of input")

# EVAL
def eval_or(ast, master):
  if ast[0] == 'OR':
    l = ast[1]
    r = ast[2]
    res1 = eval_or(l, master)
    res2 = eval_or(r, master)
    res1.update(res2)
    return res1
  else:
    return eval_unary(ast, master)

def eval_unary(ast, master):
  if ast[0] == 'FROM':
    store = ast[1]
    v = ast[2]
    res = eval_or(v, master)
    out = {}

    for k in res:
      if master[res[k][0]]['from'].lower() == store.lower():
        out[k] = res[k]

    return out
  elif ast[0] == 'OVER' or ast[0] == 'UNDER':
    price = int(ast[1])
    v = ast[2]
    res = eval_or(v, master)
    out = {}

    for k in res:
      item_price = master[res[k][0]]['price']
      item_price = re.match('\$?(\d+(\.\d+)?)', item_price)
      if not item_price:
        continue
      else:
        as_num = float(item_price.group(1))
        if ast[0] == 'OVER':
          if as_num > price:
            out[k] = res[k]
        elif ast[0] == 'UNDER':
          if as_num < price:
            out[k] = res[k]
    return out
  else:
    return eval_and(ast, master)


def eval_and(ast, master):
  if not ast[0] == 'AND':
    return eval_id(ast, master)
  else:
    results1 = eval_or(ast[1], master).items()
    results2 = eval_or(ast[2], master).items()
    return dict(results1 & results2)


def eval_id(ast, master):
  if ast[0] == 'ID':
    kw = ast[1]  # the search term
    return dict([(i + 1, (k, master[k]['price'])) for i, k in enumerate(master)
                 if kw in k.lower()])
  elif ast[0] == 'WC':
    if ast[1] == 'all':  # just return everything
      return dict([(i + 1, (k, master[k]['price']))
                            for i, k in enumerate(master)])
  else:
    raise SyntaxError("Unexpected Token Found")


def print_search_results(search_tuples):
  print("RESULTS FOUND: %d" % (len(search_tuples)))
  print("-------------------------")
  for k, v in search_tuples.items():
    print("%d | %s: %s" % (k, v[0], v[1]))
  print("-------------------------")


def query_master(master):
  search_tuples = {}
  while not search_tuples:
    query = input(
      "Valid operators include &, |, :, *, <, >\nEnter a search term: "
    ).lower()

    try:
      keywords = tokenize(query)
      (_, ast) = parse_or(keywords)
      search_tuples = eval_or(ast, master)
    except:
      print("An error occured. Please refine your search and try again.")
      continue

    # if search yielded no results
    if not search_tuples:
      print("No search results found. Try again.")
      continue

  print_search_results(search_tuples)
  return search_tuples

# m = scrape_arket_sale()
# x = tokenize('<100 :Arket *')
# print(x)
# (_, ast) = parse_or(x)
# print(ast)
# res = eval_or(ast, m)
# print(res)

# x = tokenize(':Arket <100 *')
# print(x)
# (_, ast) = parse_or(x)
# print(ast)
# res = eval_or(ast, m)
# print(res)