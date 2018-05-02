states_needed = set(['mt','wa','or','id','nv','ut'])
stations = {}
stations['kone'] = set(['id','nv','ut'])
stations['ktwo'] = set(['wa','id','mt'])
stations['kthree'] = set(['or','nv','ca'])
stations['kfour'] = set(['nv','ut'])
stations['kfive'] = set(['ca','az'])
final_stations = set()
while states_needed:
    best_station = None
    states_coverd = set()
    for station,states_for_station in stations.items():
        coverd = states_needed & states_for_station
        if len(coverd)>len(states_coverd):
            best_station = station
            states_coverd = coverd

    states_needed -= states_coverd
    final_stations.add(best_station)

print(final_stations)
