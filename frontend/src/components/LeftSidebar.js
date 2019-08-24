import React, { Component } from "react";
import { Switch, FormGroup, Divider, FocusStyleManager, H4, Spinner } from "@blueprintjs/core";
import "./Component.css";

// contains a scrollable list of sources to toggle/filter by
class LeftSidebar extends Component {

    PLACEHOLDER_SOURCES_NUM = 8;

    constructor(props) {
        super(props)

        FocusStyleManager.onlyShowFocusOnTabs();
    }

    // buffer rending when fetching articles
    renderSourcesPlaceholders(placeholdersNum) {
        var placeholders = [];

        for (var i = 0; i < placeholdersNum; i++) {
            placeholders.push(
                <Spinner key = {i} intent = "warning" size = { Spinner.SIZE_SMALL } />
            );
        }

        return placeholders;
    }

    // renders all sources in database
    renderSourcesActual(sources) {

        var renderedSources = [];

        for (var i = 0; i < sources.length; i++) {
            var source = sources[i];
            renderedSources.push(
                <Switch key = {source} className = "bp3-dark bp3-text-small"
                    defaultChecked = {true} large = {false} label = {source}
                    onChange = { this.props.updateHidden.bind(this, source) }
                />
            );
        }

        return (
            <div className = "rendered-sources">
                { renderedSources }
            </div>
        );
    }

    // renders sources
    renderSources() {
        if (this.props.sources === null) {
            return this.renderSourcesPlaceholders(this.PLACEHOLDER_SOURCES_NUM);
        } else {
            return this.renderSourcesActual(this.props.sources);
        }
    }

    render() {
        return (
            <FormGroup className = "bp3-dark form-group">
                <H4>Sources</H4>
                <Divider className = "divider"/>
                { this.renderSources() }
                <Divider className = "divider"/>

            </FormGroup>
        );
    }
}

export default LeftSidebar;
