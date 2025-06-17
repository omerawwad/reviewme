import React from "react";
import "../../styles/Review.css";
import PropTypes from "prop-types";
import { FaRegShareFromSquare } from "react-icons/fa6";
import { RatingGroup } from "@chakra-ui/react";
import { Provider } from "../ui/provider";

function Review({ review }) {
  return (
    <div className="review-card">
      <div className="review-card-header">
        <div className="review-card-header-title">
          <span className="review-title">{review.title}</span>
        </div>
        <div className="review-card-header-actions">
          <StarRating rating={review.rating} />
          <FaRegShareFromSquare className="share-icon" />
        </div>
      </div>

      <div className="review-card-info">
        <span className="review-author">@{review.user}</span>
        <span>-</span>

        <span className="review-date">
          {new Date(review.created_at).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short",
            year: "numeric",
          })}
        </span>
      </div>
      <div className="review-card-body">
        <span className="review-description">{review.description}</span>
      </div>
    </div>
  );
}

Review.propTypes = {
  review: PropTypes.shape({
    title: PropTypes.string.isRequired,
    user: PropTypes.string.isRequired,
    created_at: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    rating: PropTypes.number.isRequired,
  }).isRequired,
};

function StarRating({ rating = 0 }) {
  return (
    <Provider>
      <RatingGroup.Root
        readOnly
        count={5}
        defaultValue={rating}
        size="sm"
        colorPalette={"yellow"}
      >
        <RatingGroup.HiddenInput />
        <RatingGroup.Control />
      </RatingGroup.Root>
    </Provider>
  );
}

export default Review;
