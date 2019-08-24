import React, { Component } from "react";
import { Alignment, Navbar, NavbarGroup, Tab, Tabs, FocusStyleManager } from "@blueprintjs/core";

// top nav bar, allows the selection of articles based on the subject (Tech, Science, etc.)
class TopNavbar extends Component {

    // by default topic is General
    constructor(props) {
        super(props)

        this.state = {
            current_catagory: "General"
        }

        this.change_tab = this.change_tab.bind(this);
        FocusStyleManager.onlyShowFocusOnTabs();
    }

    // change tab to a selected tab
    change_tab(new_tab_id) {
        this.setState( { current_catagory: new_tab_id } );
    }

    // all catagories in tabbar
    render() {
        return (
            <Navbar className = "bp3-dark top-tabbar">
                <NavbarGroup align = { Alignment.LEFT }>
                    <Tabs
                        animate = { true }
                        large = { true }
                        onChange = { this.change_tab }
                        selectedTabId = { this.state.current_catagory }
                    >
                        <Tab id = "General" title = "General"/>
                        <Tab id = "Business" title = "Business"/>
                        <Tab id = "Technology" title = "Technology"/>
                        <Tab id = "Science" title = "Science"/>
                        <Tab id = "Sports" title = "Sports"/>
                        <Tab id = "Health" title = "Health"/>
                        <Tab id = "Entertainment" title = "Entertainment" />
                    </Tabs>
                </NavbarGroup>
            </Navbar>
        );
    }
}

export default TopNavbar;
