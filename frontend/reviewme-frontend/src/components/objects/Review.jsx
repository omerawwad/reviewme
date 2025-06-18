import React from "react";
import "../../styles/Review.css";
import PropTypes from "prop-types";
import { FaRegShareFromSquare } from "react-icons/fa6";
import { FaHeart } from "react-icons/fa";
import { RatingGroup } from "@chakra-ui/react";
import { Provider } from "../ui/provider";
import { LightMode } from "../ui/color-mode";

function Review({ review }) {
  return (
    <div className="review-card">
      <div className="review-card-header">
        <div className="review-card-header-title">
          <span className="review-title">{review.title}</span>
        </div>
        <div className="review-card-header-actions">
          <ReviewLikes liked={review.liked} totalLikes={review.total_likes} />
          <StarRating rating={review.rating} />
          <FaRegShareFromSquare className="share-icon" />
        </div>
      </div>

      <div className="review-card-info">
        <span className="review-author">
          {review.user == "Anonymous" ? "Anonymous" : `@${review.user}`}
        </span>
        <span>-</span>

        <span className="review-date">
          {new Date(review.created_at).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short",
            year: "numeric",
          })}
        </span>
      </div>

      {review.item && (
        <div className="review-item-intro">
          <span className="review-item-intro-text">REVIEW ON </span>
          <span className="review-item-intro-name">
            {review.item.name ? review.item.name : "Item"}
          </span>
        </div>
      )}

      <div className="review-card-body">
        <span className="review-description">{review.description}</span>
      </div>
      {review.media && review.media.length > 0 && (
        <ReviewMedia media={review.media} />
      )}
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
      <LightMode>
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
      </LightMode>
    </Provider>
  );
}

function ReviewLikes({ liked, onClick, totalLikes }) {
  return (
    <div className="like-button-container">
      <span className="like-count">{totalLikes > 0 ? totalLikes : 0}</span>

      <FaHeart className="like-icon" />
    </div>
  );
}

function ReviewMedia({ media }) {
  return (
    <div className="review-media">
      {media.map((item, index) => (
        <img
          key={index}
          src={item}
          alt={item.alt || "Review media"}
          className="review-media-item"
        />
      ))}
    </div>
  );
}

export default Review;
