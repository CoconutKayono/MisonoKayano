问：在脚本中通过变量缓存的小火人在调用时判nil
答：ouyinActor在用户切换火人的时候，会被销毁，尽量避免直接在Lua中使用DouyinActor，如果需要缓存可以使用 `DouyinActor.actorID`，并通过`DouyinActorService.GetActorById(actorID)`来获取DouyinActor

