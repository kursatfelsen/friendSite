from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from django.core.exceptions import ObjectDoesNotExist
import datetime


def k_means_event(friend):
    #print("girdi")
    scaler = StandardScaler()
    array = []
    labels = []
        
    n_clusters = len(friend.attending_set.all())//4 + 1
    #print("n_clusters:")
    #print(n_clusters)
    for item in friend.attending_set.all():
        event = item
        labels.append(event.id)
        #print(event.id)
        array_item = [int(event.type), event.start_date.hour, event.start_date.weekday()]
        array.append(array_item)

    scaled_events = scaler.fit_transform(array)
    #print(scaled_events)
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters,
                    n_init=10, max_iter=200)
    event_clusters = kmeans.fit(scaled_events).labels_
    cluster_labels = [[] for i in range(n_clusters)]

    for i, j in enumerate(event_clusters):
        cluster_labels[j].append(labels[i])

    #print("event_clusters")
    #print(event_clusters)
    #print("cluster_labels")
    #print(cluster_labels)
    #print("kmeans")
    #print(kmeans)
    #print(kmeans.cluster_centers_)

    return event_clusters, kmeans, cluster_labels
