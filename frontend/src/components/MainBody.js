import React, { Component } from "react";
import { H4, Card, Text, Elevation, FocusStyleManager, Divider, Spinner } from "@blueprintjs/core";
import Masonry from "react-masonry-css";
import "./Component.css";

// contains masonry layout of summarized articles
class MainBody extends Component {

    // used to calculate time published age
    SECONDS_MIN = 60;
    SECONDS_HOUR = 3600;
    SECONDS_DAY = 86400;

    constructor(props) {
        super(props);

        FocusStyleManager.onlyShowFocusOnTabs();
    }

    // click article to go to full article
    followUrl(articleUrl) {
        window.open(articleUrl, "_blank");
    }

    // calculates article age based on time published and current time
    getArticleAge(publishedAt) {

        var currentTime = Math.round((new Date()).getTime()/1000);
        var secondsPast =  parseInt(currentTime - publishedAt);

        if (secondsPast <= this.SECONDS_MIN){ // posted less than a minute ago
            return "now";
        } else if (secondsPast < this.SECONDS_HOUR) { // posted in the past hour
            return parseInt(secondsPast/this.SECONDS_MIN) + "m";
        } else if (secondsPast < this.SECONDS_DAY) { // posted in the the last dat
            return parseInt(secondsPast/this.SECONDS_HOUR) + "h";
        } else if (secondsPast >= this.SECONDS_DAY) {
            return parseInt(secondsPast/this.SECONDS_DAY) + "d";
        }

        return " recent";

    }

    // creates all article cards
    renderArticles() {
        var articles = [];

        if (this.props.articles === null || this.props.hidden === null) {

            for (var j = 0; j < 12; j++) {
                articles.push(
                    <Card key = {j} className = "bp3-dark" interactive = { true } elevation = { Elevation.TWO } >
                        <Spinner intent = "warning" size = { Spinner.SIZE_LARGE }></Spinner>
                    </Card>
                );
            }

        } else {

            for (var i = 0; i < this.props.articles.length; i++) {
                if (this.props.articles[i] != null) {
                    let article = this.props.articles[i];
                    let url = article.Url;
                    if (!this.props.hidden[article.Source]) { // if not hidden
                        articles.push(
                            <Card key = { article.Hash } className = "bp3-dark"
                            interactive = { true } elevation = { Elevation.TWO }
                            onClick = { () => this.followUrl(url) }
                            >
                                <H4 className = "card-title">{ article.Title } ({article.Source}) - { this.getArticleAge(article.DatePublish) }</H4>
                                <Divider className = "divider" />
                                <Text className = "card-text">{ article.Summary }</Text>
                            </Card>
                        )
                    }
                }
            }

        }

        return articles;
    }

    // renders articles in masonry format
    render() {
        return (
            <Masonry breakpointCols = { {default: 3} } className = "my-masonry-grid" columnClassName = "my-masonry-grid_column">
                { this.renderArticles() }
            </Masonry>
        );
    }
}

export default MainBody;
