# plexmusic-rating-sync

## Proof of Concept
Proof of concept currently bi-directionally syncs a 1-10 rating value from the iD3 "Publisher" tag to the Plex music "userRating". It starts by importing first then tries exporting. It currently skips any sync when any errors occur which can be either an incorrectly loaded tag or tring to overwrite an existing tag.

Roadmap
Feature Phase
- [ ] Fully implement and document sync options
  - [ ] ID3 tags override Plex (Import Mode)
  - [ ] Plex overrides ID3 Tags (Export Mode)
  - [ ] Never overwrite tags & report conflicts
  - [ ] No tag writing but export intentions (Report Mode)
- [ ] Load settings from cfg file + interactive cli setup kind of like rclone.
  - [ ] Initialize cfg file by requesting token via web UI.
- [ ] Export process details to log
  - [ ] Verbosity levels  
 
Build Phase
- [ ] Implement pyinstaller build pipeline
- [ ] Update process?
- [ ] Test
