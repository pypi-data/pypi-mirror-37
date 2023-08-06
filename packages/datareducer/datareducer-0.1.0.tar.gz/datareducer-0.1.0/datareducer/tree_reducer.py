from typing import Dict, List, Any, Callable

def modifyChild(parent: Dict, key: str) -> Dict:
  child = parent.get(key, None)
  if child is not None:
    child['cnt'] += 1
  else:
    child = {'cnt': 1}
    parent[key] = child

  return child

def recursionOnChildren(parent: Dict, keys: List[Any]) -> None:
  if keys:
    k = keys.pop()
    child = modifyChild(parent, k)
    if keys:
      recursionOnChildren(child, keys)
    else:
      return

def apply(data: List[Any], func: Callable[[Any], Any], tree=None) -> Dict:
  if tree is None:
    tree = {}

  for i in data:
    recursionOnChildren(tree, func(i))

  return  tree

class exports: 
  apply = apply
