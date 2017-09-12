# Usage/Testing of Travel

#### Initialize API with Travel class
##### Code:
<pre><code>test_travel = travel.Travel()
</pre></code>

#### Get travel time to a given destination
##### Code:
<pre><code>travel_time = test_travel.get_travel_time("Krona, Kongsberg", "bicycling", "en")
</pre></code>

##### Returns dictionary on the form:
<pre><code>{'destination_address': 'Hasbergs vei 36, 3616 Kongsberg, Norway',
 'destination_name': 'Krona - Kongsberg kultur- og kunnskapssenter',
 'distance': '508 km',
 'duration': '1 day 12 hours',
 'origin': 'Borggata 2, 5417 Stord, Norway',
 'travel_mode': 'bicycling'}
</pre></code>
