import React, { Component } from "react";
import TopNavbar from "./components/TopNavbar"
import LeftSidebar from "./components/LeftSidebar"
import MainBody from "./components/MainBody"
import OpenSocket from "socket.io-client";
import "./App.css";

var BOTTOM_INDICATOR = 0.50;
var REQUEST_NEW_ARTICLES_TIMEOUT = 1000;

var INIT_CLIENT_ARTICLES_EV = "a";
var REQUEST_NEW_ARTICLES_EV = "b";
var UPDATE_CLIENT_ARTICLES_EV = "c";


// main app contains all components
class App extends Component {

    scrollable = null;
    socket = null;

    state = {
        articles: null,
        sources: null,
        hidden: null,
        shouldUpdate: true
    }

    constructor(props) {
        super(props);

        this.initArticles = this.initArticles.bind(this);
        this.updateHidden = this.updateHidden.bind(this);
        this.requestNewArticles = this.requestNewArticles.bind(this);
        this.updateArticles = this.updateArticles.bind(this);
        this.handleScroll = this.handleScroll.bind(this);

        var socket = OpenSocket("http://localhost:8080");

        this.socket = socket;
        this.socket.on(INIT_CLIENT_ARTICLES_EV, this.initArticles);
        this.socket.on(UPDATE_CLIENT_ARTICLES_EV, this.updateArticles);
    }

    render() {
        return (
            <div className = "App">
                <div className = "left-sidebar">
                    <LeftSidebar sources = {this.state.sources} updateHidden = {this.updateHidden}/>
                </div>
                <div className = "top-navbar">
                    <TopNavbar />
                </div>
                <div id = "main-body" className = "main-body" ref = {(scrollable) => { this.scrollable = scrollable; }} onScroll = { this.handleScroll }>
                    <MainBody articles = {this.state.articles} hidden = {this.state.hidden}/>
                </div>
            </div>
        );
    }

    // requests new articles from server
    requestNewArticles() {
        this.socket.emit(REQUEST_NEW_ARTICLES_EV);
        this.setState ( { shouldUpdate: false });

        setTimeout(function(){
            this.setState( { shouldUpdate: true } );
        }.bind(this), REQUEST_NEW_ARTICLES_TIMEOUT);
    }

    // checks to see if scrolled to bottom, if there, requests aritcles from server
    handleScroll() {
        var e = document.getElementsByClassName("main-body")[0];
        if ((e.scrollTop + e.clientHeight)/(e.scrollHeight) >= BOTTOM_INDICATOR) {
            if (this.state.articles != null && this.state.shouldUpdate) {
                this.requestNewArticles();
            }
        }
    }

    // updates articles on page with articles from server
    updateArticles(data) {
        var articles = this.state.articles;

        for (var i = 0; i < data.length; i++) {
            articles.push(data[i]);
        }

        this.setState( { articles: articles });
        this.updateSoures();
    }

    // hides articles based on filters set
    updateHidden(source) {
        var hidden = this.state.hidden;
        hidden[source] = !hidden[source];
        this.setState( { hidden: hidden } );
    }

    initHidden() {
        var hidden = {};

        for (var i = 0; i < this.state.sources.length; i++) {
            var source = this.state.sources[i];
            hidden[source] = false;
        }

        this.setState({ hidden: hidden });
    }

    // updates sources availabe to toggle
    updateSoures() {
        var uniqueSources = new Set();
        for (var i = 0; i < this.state.articles.length; i++) {
            var article = this.state.articles[i];
            uniqueSources.add(article.Source);
        }

        var uniqueSourcesArr = Array.from(uniqueSources);
        var sources = Array.sort(uniqueSourcesArr);

        this.setState({ sources: sources });
        this.initHidden();
    }

    // adds article to page
    initArticles(data) {
        this.setState({ articles: data });
        this.updateSoures();
    }

}

export default App;
