from __future__ import print_function, division
import pickle
from pdb import set_trace
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
from collections import Counter
from sklearn import svm
import matplotlib.pyplot as plt
import time
import os
from demos import cmd
import urllib2
import random

def loadfile(f1,f2):
    with open("./" + str(f1), "r") as csvfile:
        content1 = [x for x in csv.reader(csvfile, delimiter=',')]

    with open("./" + str(f2), "r") as csvfile:
        content2 = [x for x in csv.reader(csvfile, delimiter=',')]
    fields = ["Document Title", "Abstract", "Year", "PDF Link", "Authors", "Source", "label", "Round 2"]
    fields2 = ["Document Title", "Abstract", "Year", "PDF Link"]
    body1={}
    body2={}

    header1 = content1[0]
    for field in fields:
        ind = header1.index(field)
        body1[field] = [c[ind] for c in content1[1:]]

    header2 = content2[0]
    for field in fields2:
        ind = header2.index(field)
        body2[field] = [c[ind] for c in content2[1:]]

    body2["title"]=map(str.lower,body2["Document Title"])
    body2["title"] = map(str.strip, body2["title"])
    for i,title in enumerate(body1["Document Title"]):
        try:
            id=body2["title"].index(title.lower().strip())
            body1["Abstract"][i]=body2["Abstract"][id]
            body1["Year"][i] = body2["Year"][id]
            body1["PDF Link"][i] = body2["PDF Link"][id]
        except:
            pass

    with open("./out.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(fields)
        ## sort before export
        ##
        for ind in xrange(len(body1["Year"])):
            csvwriter.writerow([body1[field][ind] for field in fields])

    return

def searchieee(f1):

    with open("./" + str(f1), "r") as csvfile:
        content1 = [x for x in csv.reader(csvfile, delimiter=',')]
    fields = ["Document Title", "Abstract", "Year", "PDF Link", "Authors", "Source", "label", "Round 2"]
    body1 = {}
    header1 = content1[0]
    for field in fields:
        ind = header1.index(field)
        body1[field] = [c[ind].strip() for c in content1[1:]]

    for i, title in enumerate(body1["Document Title"]):
        if body1["Year"][i]=="NA":
            title=title.split("\n")[0].strip()
            qref = "http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?ti=" + title +"&hc=1&rs=1"
            req = urllib2.Request(qref)
            req.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
            response = urllib2.urlopen(req)
            texts = response.read()

            if "<Error>" in texts:
                body1["Year"][i] = "notIEEE"
                continue
            try:
                ab=texts.split("<abstract>")[1]
                ab = ab.split("</abstract>")[0]
                ab = ab.split("<![CDATA[")[1]
                ab = ab.split("]]>")[0].strip()
                body1["Abstract"][i]=ab
            except:
                pass

            try:
                ab = texts.split("<py>")[1]
                ab = ab.split("</py>")[0]
                ab = ab.split("<![CDATA[")[1]
                ab = ab.split("]]>")[0].strip()
                body1["Year"][i] = ab
            except:
                pass

            try:
                ab = texts.split("<pdf>")[1]
                ab = ab.split("</pdf>")[0]
                ab = ab.split("<![CDATA[")[1]
                ab = ab.split("]]>")[0].strip()
                body1["PDF Link"][i] = ab
            except:
                pass

            with open("./out.csv", "wb") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(fields)
                ## sort before export
                ##
                for ind in xrange(len(body1["Year"])):
                    csvwriter.writerow([body1[field][ind] for field in fields])

            time.sleep(random.randint(2,10))

def searchacm(f1):

    with open("./" + str(f1), "r") as csvfile:
        content1 = [x for x in csv.reader(csvfile, delimiter=',')]
    fields = ["Document Title", "Abstract", "Year", "PDF Link", "Authors", "Source", "label", "Round 2"]
    body1 = {}
    header1 = content1[0]
    for field in fields:
        ind = header1.index(field)
        body1[field] = [c[ind].strip() for c in content1[1:]]

    for i, title in enumerate(body1["Document Title"]):
        if body1["Year"][i]=="notIEEE":
            title=title.split("\n")[0].strip()
            qref = "http://dl.acm.org/results.cfm?query=acmdlTitle:(" + "%252B" + "%20%252B".join(
                [j.strip("?:,.\"\'") for j in title.split()]) + ")&within=owners.owner=GUIDE"
            req = urllib2.Request(qref)
            req.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
            response = urllib2.urlopen(req)
            texts = response.read()

            try:
                ab=texts.split("\" target=\"_self\">")[0]
                ab = ab.split("<a href=\"")[-1].strip()
                pdf = "http://dl.acm.org/citation.cfm?" + ab.split("citation.cfm?")[1]
                ab="http://dl.acm.org/tab_abstract.cfm?"+ab.split("citation.cfm?")[1]
                req0 = urllib2.Request(ab)
                req0.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
                response0 = urllib2.urlopen(req0)
                body1["Abstract"][i] = response0.read().split("<div style=\"display:inline\">")[1].split("</div>")[0].strip()
                body1["PDF Link"][i] = pdf
            except:
                body1["Year"][i] = "notACM"
                continue

            try:
                ab = texts.split("<span class=\"publicationDate\">")[1]
                ab = ab.split("</span>")[0].strip()
                body1["Year"][i] = [s for s in ab.split() if s.isdigit()][-1]
            except:
                pass



            with open("./out.csv", "wb") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(fields)
                ## sort before export
                ##
                for ind in xrange(len(body1["Year"])):
                    csvwriter.writerow([body1[field][ind] for field in fields])

            time.sleep(random.randint(2, 10))

def searchacm2(f1):

    with open("./" + str(f1), "r") as csvfile:
        content1 = [x for x in csv.reader(csvfile, delimiter=',')]
    fields = ["Document Title", "Abstract", "Year", "PDF Link", "Authors", "Source", "label", "Round 2"]
    body1 = {}
    header1 = content1[0]
    for field in fields:
        ind = header1.index(field)
        body1[field] = [c[ind].strip() for c in content1[1:]]

    for i, title in enumerate(body1["Document Title"]):
        if "http://dl.acm.org/" in body1["PDF Link"][i]:
            title=title.split("\n")[0].strip()
            qref = "http://dl.acm.org/results.cfm?query=acmdlTitle:(" + "%252B"+"%20%252B".join([j.strip("?:,.\"\'") for j in title.split()]) +")&within=owners.owner=GUIDE"
            req = urllib2.Request(qref)
            req.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
            response = urllib2.urlopen(req)
            texts = response.read()
            try:
                ab=texts.split("\" target=\"_self\">")[0]
                ab = ab.split("<a href=\"")[-1].strip()
                pdf = "http://dl.acm.org/citation.cfm?" + ab.split("citation.cfm?")[1]
                ab="http://dl.acm.org/tab_abstract.cfm?"+ab.split("citation.cfm?")[1]
                req0 = urllib2.Request(ab)
                req0.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
                response0 = urllib2.urlopen(req0)
                body1["Abstract"][i] = response0.read().split("<div style=\"display:inline\">")[1].split("</div>")[0].strip()
                body1["PDF Link"][i] = pdf
            except:
                body1["Year"][i] = "notACM"
                continue

            try:
                ab = texts.split("<span class=\"publicationDate\">")[1]
                ab = ab.split("</span>")[0].strip()
                body1["Year"][i] = [s for s in ab.split() if s.isdigit()][-1]
            except:
                pass



            with open("./out2.csv", "wb") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(fields)
                ## sort before export
                ##
                for ind in xrange(len(body1["Year"])):
                    csvwriter.writerow([body1[field][ind] for field in fields])

            time.sleep(random.randint(2, 10))




def searchcrossref(f1):

    with open("./" + str(f1), "r") as csvfile:
        content1 = [x for x in csv.reader(csvfile, delimiter=',')]
    fields = ["Document Title", "Abstract", "Year", "PDF Link", "Authors", "Source", "label", "Round 2"]
    body1 = {}
    header1 = content1[0]
    for field in fields:
        ind = header1.index(field)
        body1[field] = [c[ind].strip() for c in content1[1:]]

    for i, title in enumerate(body1["Document Title"]):
        if body1["Year"][i]=="notIEEE":
            title=title.split("\n")[0].strip()
            qref = "https://api.crossref.org/works?rows=1&query.title=" + title
            req = urllib2.Request(qref)
            req.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
            response = urllib2.urlopen(req)
            texts = response.read()


            try:
                tt=texts.split("\"title\":[\"")[1]
                tt=tt.split("\"]")[0].strip()
                if not title.lower() in tt.lower():
                    body1["Year"][i] = "notCrossRef"
                    continue
            except:
                body1["Year"][i] = "notCrossRef"
                continue

            try:
                ab=texts.split("<abstract>")[1]
                ab = ab.split("</abstract>")[0]
                ab = ab.split("<![CDATA[")[1]
                ab = ab.split("]]>")[0].strip()
                body1["Abstract"][i]=ab
            except:
                pass

            try:
                ab = texts.split("<py>")[1]
                ab = ab.split("</py>")[0]
                ab = ab.split("<![CDATA[")[1]
                ab = ab.split("]]>")[0].strip()
                body1["Year"][i] = ab
            except:
                pass

            try:
                ab = texts.split("<pdf>")[1]
                ab = ab.split("</pdf>")[0]
                ab = ab.split("<![CDATA[")[1]
                ab = ab.split("]]>")[0].strip()
                body1["PDF Link"][i] = ab
            except:
                pass

            with open("./out.csv", "wb") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(fields)
                ## sort before export
                ##
                for ind in xrange(len(body1["Year"])):
                    csvwriter.writerow([body1[field][ind] for field in fields])

            time.sleep(random.randint(2, 10))

if __name__ == "__main__":
    eval(cmd())