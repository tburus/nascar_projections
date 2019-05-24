# nascar_projections
Create weekly NASCAR projections and find optimal fantasy lineups for DraftKings and FanDuel

The workflow is as follows:

	(1) Scrape data -- you need up to four years prior to the current in order to have enough past track results

	(2) Entry list -- I have not included my entry list program because it contains a private API key. You can 
		generate your own entry list using data available online

	(3) Make initial projections -- fantasy_proj.py creates projections for DraftKings and FanDuel based off 
		of last four races in the season and last for at the track

	(4) Summarize initial projections -- use roster_create.py

	(5) Optimize projections -- get one optimal projection for each site using *_opti_lineup.py files. Get 
		different (possibly sub-) optimal lineups using opti_stop.py

	(6) Scrape qualifying data -- get qualifying results using qualifying.py

	(7) Adjust projections post-qualifying -- adjust projections per site using *_fantasy_proj_pq.py

	(8) Summarize post-qualifying projections -- use roster_create_pq.py

	(9) Make final projections -- re-run optimization programs with post-qualifying data
