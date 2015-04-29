from pickle import load
from paper.text import tex_renderer, write_file

with open("build/data.pickle") as f:
    data = load(f)

template = tex_renderer.get_template("temperature.tex")

def table_data(s):

    _ = {"id": s["id"]}
    d = s["core"]

    # Get number of grains
    for i in ("n_opx","n_cpx"):
        arr = [v["single"][i] for v in d.values()]
        # They should be the same for all thermometers
        assert all(x == arr[0] for x in arr)
        _[i] = arr[0]

    _.update({k: v["single"]["val"]
        for k,v in d.items()})

    _["id"] = s["id"]
    return _

text = template.render(
        samples=[table_data(s) for s in data])
write_file("build/temperatures.tex", text)
