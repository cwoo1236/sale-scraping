def parse_or(tokens):
  (t, left) = parse_and(tokens)
  if t and t[0] == 'OR':
    (tt, right) = parse_or(t[1:])
    return (tt, ('OR', left, right))
  else:
    return (t, left)


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


def eval_or(ast, master):
  if ast[0] == 'OR':
    l = ast[1]
    r = ast[2]
    res1 = eval_or(l, master)
    res2 = eval_or(r, master)
    res1.update(res2)
    return res1
  elif ast[0] == 'AND':
    return eval_and(ast, master)
  elif 'ID' in ast[0]:
    return eval_id(ast, master)


def eval_id(ast, master):
  if not ast[0] == 'ID':
    raise SyntaxError("Not ID")
  else:
    kw = ast[1]  # the search term
    return dict([(i + 1, (k, master[k]['price'])) for i, k in enumerate(master)
                 if kw in k.lower()])


def eval_and(ast, master):
  if not ast[0] == 'AND':
    raise SyntaxError("Expected AND; got %s" % (ast[0]))
  else:
    results1 = eval_id(ast[1], master).items()
    results2 = eval_id(ast[2], master).items()
    return dict(results1 & results2)


def tokenize(input):
  fun = lambda x: 'OR' if x == '|' else 'AND' if x == '&' else ('ID', x)
  tokens = input.split(' ')
  return list(map(fun, tokens))


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
      "Enter a keyword to search for, or press 'Enter' again to see all items: "
    ).lower()

    if not query:
      search_tuples = dict([(i + 1, (k, master[k]['price']))
                            for i, k in enumerate(master)])
      break

    keywords = tokenize(query)
    (_, ast) = parse_or(keywords)

    search_tuples = eval_or(ast, master)
    # Search yielded no results
    if not search_tuples:
      print("No search results found. Try again.")
      continue

  print_search_results(search_tuples)
  return search_tuples


def print_search_results(search_tuples):
  print("RESULTS FOUND: %d" % (len(search_tuples)))
  print("-------------------------")
  for k, v in search_tuples.items():
    print("%d | %s: %s" % (k, v[0], v[1]))
  print("-------------------------")
