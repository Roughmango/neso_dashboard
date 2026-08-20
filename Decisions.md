The following major decisions for the project are being recorded here:

Database Design: The decisions was made to have a primary id for all data recorded be the period the data is from
and when the data was actually recorded into the database, so the frequency of the data being added can be seen.
The decision was made for this to be the primary key as a top down database design could be used that way, with both
national and regional data able to have a connection through this key.

Data fetch pipeline and automation: A pipeline has been set up using the fetch, transform and validate python files to fetch, transform and add data to the online database
and then validate once it has been done so to flag any issues. This pipeline is then set up to take place every 15 minutes through
github actions, which automates the task. Although it does not always perform the task every 15 minutes, it was felt
this was the simplest way to automate due to it being built into github which was already being used as version control
for this project.

Database choice: For the database, supabase is being used as it is allows for free online database that the data can easily be stored to.
As such postgresql has to be used as it is compatible with the website.

First iteration of XGBoost model: For my first attempt at predicting the intensity I decided to use XGBoost as it has
readily available libraries so will be easy to implement within my project. For the first attempt specifically I just
wanted to focus on using how past intensities had been predicted and what they actually were, before moving on to using
generation mix in later models, as this will also allow me to predict regional intensities as well seeing as they don't
actual intensities. 