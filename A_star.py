"""


Written by Apolo Aggrey (apolloaggrey@students.uonbi.ac.ke.com).

(c) Copyright , All Rights Reserved. NO WARRANTY.

"""
import time
import os
##########################################
data_path = os.path.dirname(os.path.realpath(__file__))
data_path = (str(data_path)[:]+"\data.txt")
node_map = os.path.dirname(os.path.realpath(__file__))
node_map = (str(data_path)[:]+"node_map.txt")
print(data_path)
print(node_map)
#data_path = "C:\\Users\\apoll_1z1djr1\\Documents\\a_star_2\\data.txt" #modify to match the path of data.txt on your system
#node_map = "C:\\Users\\apoll_1z1djr1\\Documents\\a_star_2\\node_map.txt"#modify to match the path of mode_map.txt on your system

start = 'Arad'
goal = 'Eforie'
through = None
through2 = None
through3 = None

speed = float(0.2)
show_progress = True
units = "Kms"

###########################################


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



nodes_map = {}
"""do not modify """


def format_data(_):

    """
    creates a dict of dicts that can be recuresed over
    by the main function.

    :param _:
    """

    try:
        temp_map = {}
        global nodes_map
        data = open(data_path, mode="r")
        data2 = open(node_map, mode="w")
        for line in data:
            data2.write(line)
        pass

        data2.write('\n')
        data2.close()
        data2 = open(node_map, mode="r+")

        for line in data2:
            try:
                ((raw1), (raw2), (raw3)) = line.split()
                float(raw3)
                data2.write(raw2 + " " +
                            raw1 + " " +
                            raw3 + "\n")
                pass
            except Exception as e:
                print(e)
                print("'",line[:-1],"'"," ",end="")
                print(color.RED+"was EXCLUDED from the search\n")
            pass
        pass

        data.close()
        data2.close()
        data2 = open(node_map, mode="r")

        for line in data2:
            # noinspection PyBroadException
            try:
                ((raw1), (raw2), (raw3)) = line.split()
                temp_map.setdefault(raw1,
                {}).update({raw2: float(raw3)})
            except Exception:
                pass
                # print(e)
                # print(line[:-1]," ",end="")
                # print("Excluded from search\n")
            pass
        pass

        data2.close()

        spacing = 0
        data2 = open(node_map, mode="w")
        data2.write("{")

        for node in temp_map:
            if len(node) >= spacing:
                spacing = len(node)
            pass
        pass

        for node in temp_map:
            data2.write("'" +
                        str(node) +
                        " " * (spacing - len(node)) +
                        "':" + " " +
                        str(temp_map[node]) +
                        ",\n ")
            nodes_map.setdefault(node, {}).update(temp_map[node])
            time.sleep(speed)
        pass

        data2.write("}")
    except Exception as e:
        print(color.RED+"\t\t\t\t>> ERROR ENCOUNTERED <<")
        print(color.RED+"\t\t ERROR :", e)
    pass


def a_star(map,src: object,
           dest: object,
           visited=None,
           paths=None,
           parents=None
           ) -> object:

    """

    :param map:
    :param paths:
    :param parents:
    :param visited:
    :param dest:
    :type src: object
    """
    if parents is None:
        parents = {}
    if paths is None:
        paths = {}
    if visited is None:
        visited = []
    global show_progress
    global starting

    try:
        # compatibility checks
        if src not in map:
            raise TypeError(src+color.RED+ 'the root of the shortest path tree cannot be found in the graph')
        if dest not in map:
            raise TypeError(dest+color.RED+ 'the target of the shortest path cannot be found in the graph')
            # ending condition
        if src == dest:
            # build the shortest path and display it
            path = []
            parent = dest
            while parent is not None:
                path.append(parent)
                parent = parents.get(parent, None)
            pass

            print(color.GREEN+"\n\t\tcompleted  (UTS): ", time.time())
            print(color.GREEN+"\t\ttime taken (sec): ", time.time() - starting)
            time.sleep(speed)
            print(color.BOLD+color.BLUE+'\nshortest path  : ' + str(path) + " \n"
                  "f-cost of path : " + "[" + str(paths[dest]) + "]"+ units)
            pass
            time.sleep(speed)

        else:
            # if it is the initial  run,
            # initializes the cost of start to 0
            # noinspection PyTypeChecker
            if not len(visited):
                paths[src] = float(0.0)
                if show_progress:
                    print(color.BLUE+"(f)-cost      : ","{", src, ":", paths.get(src, float('inf')),"}",units, "\n")
            pass

            # visit the neighbors

            for node in map[src]:
                # if node not in visited:
                new_distance = paths[src] + map[src][node]
                # add the h-cost to g-cost to get f-cost(new_distance)
                if new_distance < paths.get(node, float('inf')):
                    paths[node] = new_distance
                    parents[node] = src
                    # print("count :",count)
                    if show_progress:
                        time.sleep(.75)
                        print(color.BLUE+"visited paths :", paths)
                        print(color.BOLD+"(f)-cost      : ", paths.get(node, float('inf')), units,"\n")
                    pass
                pass
            pass

            # mark as visited

            visited.append(src)
            # now that all neighbors have been visited:
            # recurse
            # select the non visited node with lowest distance
            unvisited = {}

            for node in map:
                if node not in visited:
                    unvisited[node] = paths.get(node, float('inf'))
                pass
            pass
            #  select the path with least h-cost
            h_cost = min(unvisited,key=unvisited.get)
            time.sleep(speed)
            a_star(map, h_cost, dest, visited, paths, parents)

        pass

    except Exception as e:
        print("\t\t\t\t>> ERROR ENCOUNTERED <<")
        print(color.RED+"\t\t ERROR :", e)
    pass


if __name__ == "__main__":
    format_data(data_path)
    starting = float(time.time())
    print("\n\t\tstarting  (UTS): ", starting, "\n")
    if not through:
        a_star(nodes_map, start, goal)
    elif through and through2 and through3:
        a_star(nodes_map, start, through)
        a_star(nodes_map, through, through2)
        a_star(nodes_map, through2, through3)
        a_star(nodes_map, through3, goal)
        pass
    elif through and through2:
        a_star(nodes_map, start, through)
        a_star(nodes_map, through, through2)
        a_star(nodes_map, through2, goal)
        pass
    elif through:
        a_star(nodes_map, start, through)
        a_star(nodes_map, through, goal)
    pass


