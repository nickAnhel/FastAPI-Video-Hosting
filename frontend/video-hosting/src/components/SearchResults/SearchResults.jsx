import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import "./SearchResults.css"

import VideoService from '../../service/VideoService';
import PlaylistService from '../../service/PlaylistService';
import UserService from '../../service/UserService';

import VideosList from '../VideosList/VideosList';
import PlaylistsList from '../PlaylistsList/PlaylistsList';
import ChannelsList from '../ChannelsList/ChannelsList';


function SearchResults() {
    const [searchParams] = useSearchParams();
    const searchScope = searchParams.get("scope");
    const searchQuery = searchParams.get("query");

    return (
        <div className="search-results">
            {
                searchScope == "videos" &&
                <VideosList fetchVideos={VideoService.searchVideos} filters={{desc: true, query: searchQuery}} refresh={searchQuery} />
            }
            {
                searchScope == "playlists" &&
                <PlaylistsList fetchedPlaylists={PlaylistService.searchPlaylists} filters={{desc: true, query: searchQuery}} refresh={searchQuery} />
            }
            {
                searchScope == "channels" &&
                <ChannelsList fetchChannels={UserService.searchUsers} filters={{desc: true, query: searchQuery}} refresh={searchQuery} />
            }
        </div>
    )
}

export default SearchResults;