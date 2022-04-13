function remove() {
    var td = event.target.parentNode; 
      var tr = td.parentNode; // the row to be removed
      tr.parentNode.removeChild(tr);
}

function add(){
    const btn = document.createElement("tbody");
    btn.innerHTML = `<tr class="inner-box">
                                        <th scope="row">
                                            <div class="event-date">
                                                <p>8:30 AM - 9:45 AM</p>
                                            </div>
                                        </th>
                                        <td>
                                            <div class="event-wrap">
                                                <h3><a href="#">CS 326: Analysis of Algorithms</a></h3>
                                                <div class="meta">
                                                    <div class="organizers">
                                                        <a href="https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1083351" target="_blank">Michaelangelo Grigni</a>
                                                    </div>
                                                    <div class="categories">
                                                        <a href="#">Mon/Wed</a>
                                                    </div>
                                                    <div class="time">
                                                        <span></span>
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="r-no">
                                                <span>Math &amp; Science Center W201</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="primary-btn">
                                                <a class="btn btn-primary">Read More</a>
                                            </div>
                                        </td>
                                        <td>
                                            <input type="button" value="Remove" onclick="remove()">
                                        </td>
                                    </tr>`
    var day = document.getElementById("monday")
    day.appendChild(btn);
}