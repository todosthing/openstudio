import React, { Component } from "react"
import { intlShape } from "react-intl"
import PropTypes from "prop-types"
import validator from 'validator'
import { v4 } from "uuid"



class CustomerDisplayNotes extends Component {
    constructor(props) {
        super(props)
        console.log(props)
    }

    PropTypes = {
        intl: intlShape.isRequired,
    }

    componentWillMount() {
    }

    componentDidMount() {
    }


    render() {
        const customers = this.props.customers
        const notes = customers.notes
        const notes_loaded = customers.notes_loaded
        const notes_loading = customers.notes_loading

        return (
           <div>
               { (notes_loaded) ?
                (notes.data) ?
                    <div>     
                        <b>Notes</b>
                        {console.log(notes.data)}
                        <div className="direct-chat-messages">
                        {notes.data.map((note, i) => 
                            <div key={v4()}>                               
                                <div className="direct-chat-msg">
                                    <div className="direct-chat-info clearfix">
                                    <span className="direct-chat-name pull-left">{note.User}</span>
                                        <span className="direct-chat-timestamp pull-right">{note.Timestamp} {note.Time}</span>
                                    </div>
                                    <img className="direct-chat-img" src="/static/images/person.png" alt="" />
                                    <div className="direct-chat-text">
                                        {note.Note}
                                    </div>
                                </div>
                            </div>
                        )}
                        </div>
                    </div> : '' 
                : "Loading notes, please wait..."
               }
           </div>
        )
    }
}

export default CustomerDisplayNotes