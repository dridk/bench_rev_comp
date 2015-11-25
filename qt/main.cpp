#include <iostream>
#include <QCommandLineParser>
#include <QCoreApplication>
#include <QStringList>
#include <QDebug>
#include <QElapsedTimer>
#include "bench.h"
using namespace std;

int main(int argc, char **argv)
{


    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("bench");
    QCoreApplication::setApplicationVersion("1.0");

    QCommandLineParser parser;
    parser.setApplicationDescription("Qt benchmark");
    parser.addHelpOption();
    parser.addPositionalArgument("count", "the count");
    parser.addPositionalArgument("seq", "string sequence");


    parser.process(app);

    QStringList args = parser.positionalArguments();

    Bench b;



    QElapsedTimer time;

    time.start();
    b.translate(args[0].toInt(), args[1]);

    qDebug()<<"naive"<<time.elapsed();






}

