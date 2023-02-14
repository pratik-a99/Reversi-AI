import ordinaryBackup
import supervisorTest
import computer

wincount = 0
games = 20
result = []

for i in range(games):
    win = supervisorTest.supervisor(
        "ordinaryBackup", "improvedBackup1", 0.5, False)
    print(win)
    if win == "p2":
        wincount += 1
    result.append(win == "p2")

print("ordinaryBackup won " + str(wincount) +
      " times" + " out of " + str(games) + " games")
print("ordinaryBackup won " + str(wincount/games*100) + "% of the time")
print(result)
