# InsightDE-Waitless
## Samantha Mikaiel's Insight-NY-18B Data Engineering Project

A Real-Time Restaurant Wait Tracker 
[Waitless](http:/waitless.site)
[Presentation](https://www.slideshare.net/SamanthaMikaiel/samantha-mikaiel-de-ny-18b-waitless)
[DemoVideo](https://www.youtube.com/watch?v=to9YMzezwqk&feature=youtu.be)

### About Waitless
The demand for a restaurant changes cyclically. Prime meal times have longer waits than the middle of the night. Mother's Day will have more brunch reservations than a Tuesday in November. The trend continues. And when the demand to a restaurant increases the wait times at restaurants increase as well. When people are hungry, they tend to go to restaurants with shorter wait times if possible.

This pipeline allows for a resturaunt to input their current wait time in real-time, while allowing users to query the wait times of all of the restuarunts in their zip code.

### Pipeline
![alt text](https://github.com/samanthamikaiel/InsightDE-Waitless/blob/master/Pipeline.jpg?raw=true)

### Engineering Challenges
Latency - 
  Solution: Fan-out problem with creating multiple shards and using Kinesis Analytics
  
Cost - 
  Solution: Autoscaling split and merge shards as input requires
