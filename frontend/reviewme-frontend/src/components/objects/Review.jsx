import React, { use, useEffect } from "react";
import "../../styles/Review.css";
import PropTypes from "prop-types";
import { FaRegShareFromSquare } from "react-icons/fa6";
import { FaHeart } from "react-icons/fa";
import { RatingGroup } from "@chakra-ui/react";
import { Provider } from "../ui/provider";
import { LightMode } from "../ui/color-mode";
import { useNavigate } from "react-router-dom";

function Review({ review }) {
  const navigate = useNavigate();

  //   console.log(review);
  const handleLikeClick = () => {
    // Handle the like button click
    console.log("Like button clicked for review:", review.id);
    // Here you would typically call an API to like the review
  };
  const handleShareClick = () => {
    // Handle the share button click
    console.log("Share button clicked for review:", review.id);
    // Here you would typically implement sharing functionality
  };

  const handleItemClick = () => {
    // console.log("Item clicked:", review.item ? review.item.id : "No item");
    if (review.item && review.item.id) {
      navigate(`/item/${review.item.id}`, {
        state: { item: review.item },
      });
    }
  };
  return (
    <div className="review-card">
      <div className="review-card-header">
        <div className="review-card-header-title">
          <span className="review-title">{review.title}</span>
        </div>
        <div className="review-card-header-actions">
          <ReviewLikes
            liked={review.is_liked}
            totalLikes={review.total_likes}
          />
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
        <div className="review-item-intro" onClick={handleItemClick}>
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

      <LikeReviewButton liked={liked} onClick={onClick} />
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

function LikeReviewButton({ liked, onClick }) {
  return (
    <button className="like-review-button" onClick={onClick}>
      <FaHeart className={`like-icon ${liked ? "liked" : ""}`} />
    </button>
  );
}

export default Review;
