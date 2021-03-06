import React, { Component } from "react"
import { intlShape } from "react-intl"
import { v4 } from "uuid"
import PropTypes from "prop-types"

import ShopTemplate from '../../ShopTemplate'
import SchoolMenu from '../components/SchoolMenu'

import ClasscardsList from './ClasscardsList'

class Classcards extends Component {
    constructor(props) {
        super(props)
        console.log(props)
    }

    PropTypes = {
        intl: intlShape.isRequired,
        setPageTitle: PropTypes.function,
        addToCart: PropTypes.function,
        app: PropTypes.object,
        classcards: PropTypes.object,
        loaded: PropTypes.boolean,
    }

    componentWillMount() {
        this.props.setPageTitle(
            this.props.intl.formatMessage({ id: 'app.pos.products' })
        )
        if (!this.props.loaded) {
            this.props.fetchShopClasscards()
        }
    }
    
    onClickClasscard(card) {
        console.log('clicked on:')
        console.log(card)

        let item = {
           id: v4(),
           item_type: 'classcard',
           quantity: 1,
           data: card
        }

        console.log('item')
        console.log(item)
        // Check if item not yet in cart
        
        // If not yet in cart, add as a new pproduct, else increase 
        this.props.addToCart(item)
        
        // this.props.setDisplayCustomerID(id)
    }

    render() {
        return (
            <ShopTemplate app_state={this.props.app}>
                { this.props.loaded ? 
                     <SchoolMenu>
                         <br /><br />
                         <ClasscardsList classcards={this.props.classcards}
                                         onClick={this.onClickClasscard.bind(this)} />
                     </SchoolMenu> :
                     "Loading..."
                }
            </ShopTemplate>
        )
    }
}

export default Classcards
