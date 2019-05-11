// this program generates an m3u file, containing entries
// based upon the parameters specified in the code and
// outputs a file out.m3u
// it calls the mediainfo program to determine durations

#include <cstdio>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cmath>
using namespace std;

void clampint(int clamptosmall, int clamptobig , int& number) {
    if(number > clamptobig) number=clamptobig;
    else if(number < clamptosmall) number=clamptosmall;
}

int main(int argc, char* argv[]) {
    int whichtimerange = 3;
    cout << "usage: ./a [howlong in seconds] [early/late: 1-" << whichtimerange << "] [filepath1] [filepath2] ..." << endl;
    string howlong = argv[1];
    int howlongint = stoi(howlong);

    string whichtime = argv[2];
    int whichtimeint = stoi(whichtime);


    srand(time(NULL));


    vector<string> titles;
    for(int i=3;i<argc;i++) {
        string title = argv[i];
        titles.push_back(title);
    }

//    titles.push_back("a.mp4");
//    titles.push_back("b.mp4");

    vector<int> durations;
    for(int i=0; i<titles.size(); i++) {
        string abc = "mediainfo --Inform=\"General;%Duration%\" " + titles[i];

        FILE *fp = popen(abc.c_str(), "r");
        char buf[1024];

        string bufstr;
        if (fgets(buf, 1024, fp))
            bufstr = buf;

        fclose(fp);

        cout << bufstr << endl;
        durations.push_back(stoi(bufstr)/1000);
    }

    cout << "...." << durations[0] << " " << durations[1] << endl;



    ofstream out("out.m3u");

    if(out) {
        out << "#EXTM3U" << endl;
        for(int i=0; i<500; i++) {

            int actuallength = howlongint;
            if(rand()%2==0)
                actuallength += rand()%(int) (0.5*(float)howlongint);
            else {
                actuallength -= rand()%(int) (0.5*(float)howlongint);
            }
            int randomtitle = rand()%titles.size();

            int starttime = 0;
//            int offsettime = rand()%(int) (durations[randomtitle]);
            for(int j=0; j<whichtimeint; j++) {
                starttime += rand()%(int) (durations[randomtitle]/((whichtimeint)-j*0.28*whichtimeint));
            }
            clampint(durations[randomtitle]/25, durations[randomtitle] - durations[randomtitle]/25, starttime);
            int stoptime = starttime + actuallength;

            string randtitle = titles[randomtitle];
            out << "#EXTINFO:-1," << randtitle << endl
                << "#EXTVLCOPT:start-time=" << starttime << endl
                << "#EXTVLCOPT:stop-time=" << stoptime << endl
                << randtitle << endl;
        }
    }

    return 0;
}
