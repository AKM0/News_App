// AKM

var express = require("express");
var socket = require("socket.io");
var fs = require("fs");
var sqlite3 = require("sqlite3");

//command line options
var PORT_NUMBER = 8080;

var STARTING_ARTICLES_NUM = 12;
var REQUEST_ARTICLES_NUM = 12;

var INIT_CLIENT_ARTICLES_EV = "a";
var REQUEST_NEW_ARTICLES_EV = "b";
var UPDATE_CLIENT_ARTICLES_EV = "c";

var database = new sqlite3.Database("main.db", sqlite3.OPEN_READONLY);
var app = express();
var server = app.listen(PORT_NUMBER, onServerStart);
var io = socket(server);

var totalArticlesNum = 0;
var articles = [];
var articlesByClient = new Map();

io.on("connect", onSocketConnection); //when connected to a client, fire onSocketConnection

function onServerStart () {
    console.log("SERVER INITILIAZED ON PORT " + PORT_NUMBER);
    initArticles();
}

function onSocketConnection(clientConnection) {
    console.log("Client connected.")

    // send client all summarized articles
    initClientArticles(clientConnection);

    // on client request new articles (user scrolls past bottom of page), send new articles
    clientConnection.on(REQUEST_NEW_ARTICLES_EV, function() {
        updateClientArticles(clientConnection);
    });

    // on client disconnect
    clientConnection.on("disconnect", function(){
        articlesByClient.delete(clientConnection.id);
        console.log("Client disconnected.");
    });
}

function initArticles() {

    // fetch articles for db
    getTotalRows("Articles", function(err, result) {
        totalArticlesNum = result[0]["COUNT(*)"];
        getNRowsDecending("Articles", "DatePublish", STARTING_ARTICLES_NUM, function (err, result) { articles = result; } );
    });

}

// send all articles to client
function initClientArticles(clientConnection) {
    var articlesArr = [];

    for (var i = 0; i < STARTING_ARTICLES_NUM; i++) {
        articlesArr.push(articles[i]);
    }

    clientConnection.emit(INIT_CLIENT_ARTICLES_EV, articlesArr);
    articlesByClient.set(clientConnection.id, STARTING_ARTICLES_NUM);
}

// send client new articles based on which articles they have already seen
function updateClientArticles(clientConnection) {

    var currentClientArticlesNum = articlesByClient.get(clientConnection.id);
    var newClientArticlesNum = currentClientArticlesNum + REQUEST_ARTICLES_NUM;

    // do not load more than maximum articles allowed
    if (newClientArticlesNum > totalArticlesNum) {
        newClientArticlesNum = totalArticlesNum;
    }

    var articlesArr = [];

    if (articles.length < newClientArticlesNum) {

        getNRowsDecending("Articles", "DatePublish", newClientArticlesNum, function (err, result) {
            articles = result;

            for (var i = currentClientArticlesNum; i < newClientArticlesNum; i++) {
                articlesArr.push(articles[i]);
            }

            clientConnection.emit(UPDATE_CLIENT_ARTICLES_EV, articlesArr);
            articlesByClient.set(clientConnection.id, newClientArticlesNum);
        } );

    } else {

        for (var i = currentClientArticlesNum; i < newClientArticlesNum; i++) {
            articlesArr.push(articles[i]);
        }

        clientConnection.emit(UPDATE_CLIENT_ARTICLES_EV, articlesArr);
        articlesByClient.set(clientConnection.id, newClientArticlesNum);
    }
}





function getTable(tableName, callback) {
    var query = "SELECT * FROM " + tableName;
    database.all(query, [], callback);
}

function getEntireColumn(tableName, columnName) {
    var query = "SELECT " + columnName + " FROM " + tableName;
    database.all(query, [], printResults);
}

function getEntireRow(tableName, primaryKey, value) {
    var query = "SELECT * FROM " + tableName + " WHERE " + primaryKey + " = ?";
    database.all(query, [value], printResults);
}

function getNRowsDecending(tableName, sortColumn, n, callback) {

    if (n > totalArticlesNum) {
        n = totalArticlesNum;
    }

    var query = "SELECT * FROM " + tableName + " ORDER BY " + sortColumn + " DESC LIMIT " + n;

    database.all(query, [], callback);
}

function getRowValue(tableName, primaryKey, columnName, value) {
    var query = "SELECT " + columnName + " FROM " + tableName + " WHERE " + primaryKey + " = ?";
    database.all(query, [value], printResults);
}

function getTotalRows(tableName, callback) {
    var query = "SELECT COUNT(*) FROM " + tableName;
    database.all(query, [], callback);
}

function printResults(err, results) {
    console.log(results);
}
