// F. Permadi 2005.
// Highlights table row
// Copyright (C) F. Permadi
// This code is provided "as is" and without warranty of any kind.  Use at your own risk.



// These variables are for saving the original background colors
var savedStates=new Array();
var savedStateCount=0;

var savedBlockState = new Array();
var savedBlockStateCount = 0;
//var state = 'block';


/////////////////////////////////////////////////////
// This function takes an element as a parameter and 
//   returns an object which contain the saved state
//   of the element's background color.
/////////////////////////////////////////////////////
function saveBackgroundStyle(myElement)
{
  saved=new Object();
  saved.element=myElement;
  saved.className=myElement.className;
  saved.backgroundColor=myElement.style["backgroundColor"];
  return saved;   
}

/////////////////////////////////////////////////////
// This function takes an element as a parameter and 
//   returns an object which contain the saved state
//   of the element's background color.
/////////////////////////////////////////////////////
function restoreBackgroundStyle(savedState)
{
  savedState.element.style["backgroundColor"]=savedState.backgroundColor;
  if (savedState.className)
  {
    savedState.element.className=savedState.className;    
  }
}

/////////////////////////////////////////////////////
// This function is used by highlightTableRow() to find table cells (TD) node
/////////////////////////////////////////////////////
function findNode(startingNode, tagName)
{
  // on Firefox, the TD node might not be the firstChild node of the TR node
  myElement=startingNode;
  var i=0;
  while (myElement && (!myElement.tagName || (myElement.tagName && myElement.tagName!=tagName)))
  {
    myElement=startingNode.childNodes[i];
    i++;
  }  
  if (myElement && myElement.tagName && myElement.tagName==tagName)
  {
    return myElement;
  }
  // on IE, the TD node might be the firstChild node of the TR node  
  else if (startingNode.firstChild)
    return findNode(startingNode.firstChild, tagName);
  return 0;
}

/////////////////////////////////////////////////////
// Highlight table row.
// newElement could be any element nested inside the table
// highlightColor is the color of the highlight
/////////////////////////////////////////////////////
function highlightTableRowVersionA(myElement, highlightColor)
{
  var i=0;
  // Restore color of the previously highlighted row
  for (i; i<savedStateCount; i++)
  {
    restoreBackgroundStyle(savedStates[i]);          
  }
  savedStateCount=0;

  // If you don't want a particular row to be highlighted, set it's id to "header"
  if (!myElement || (myElement && myElement.id && myElement.id=="header") )
    return;
		  
  // Highlight every cell on the row
  if (myElement)
  {
    var tableRow=myElement;
    
    // Save the backgroundColor style OR the style class of the row (if defined)
    if (tableRow)
    {
      savedStates[savedStateCount]=saveBackgroundStyle(tableRow);
      savedStateCount++;
    }

    // myElement is a <TR>, then find the first TD
    var tableCell=findNode(myElement, "TD");    

    var i=0;
    // Loop through every sibling (a sibling of a cell should be a cell)
    // We then highlight every siblings
    while (tableCell)
    {
      // Make sure it's actually a cell (a TD)
      if (tableCell.tagName=="TD")
      {
        // If no style has been assigned, assign it, otherwise Netscape will 
        // behave weird.
        if (!tableCell.style)
        {
          tableCell.style={};
        }
        else
        {
          savedStates[savedStateCount]=saveBackgroundStyle(tableCell);        
          savedStateCount++;
        }
        // Assign the highlight color
        tableCell.style["backgroundColor"]=highlightColor;

        // Optional: alter cursor
        tableCell.style.cursor='default';
        i++;
      }
      // Go to the next cell in the row
      tableCell=tableCell.nextSibling;
    }
  }
}

/////////////////////////////////////////////////////
// goto Url by id of element
/////////////////////////////////////////////////////
function gotoCombinedUrl(myElement, urlpath)
{
  if (myElement && urlpath) {
      window.location.href=(urlpath + myElement.id + '/');  
  }
}

function getAndSaveBlockState(layer_ref) {
    var i=0;
    var m_state = 'unknown';
    for (i=0;i<savedBlockStateCount;i++) {
	var obj = savedBlockState[i];
	if (obj.layer_ref == layer_ref) {
	    if (obj.block_state == 'block') {
		obj.block_state = 'none';
		m_state = 'none'; 
	    } else {
		obj.block_state = 'block';
		m_state = 'block';
	    }
	}
    }
    if (m_state == 'unknown') {
	var obj = new Object();
	m_state = 'none';
	obj.block_state = m_state;
	obj.layer_ref = layer_ref;
	savedBlockState[savedBlockStateCount] = obj;
	savedBlockStateCount++;
    }

    return m_state;
}

function showhide(layer_ref) {
    var m_state;

    m_state = getAndSaveBlockState(layer_ref);
    /*
	if (state == 'block') {
	state = 'none';
    }
    else {
	state = 'block';
    }
    */

    if (document.all) { //IS IE 4 or 5 (or 6 beta)
	eval( "document.all." + layer_ref + ".style.display = m_state");
    }
    if (document.layers) { //IS NETSCAPE 4 or below
	document.layers[layer_ref].display = m_state;
    }
    if (document.getElementById &&!document.all) {
	hza = document.getElementById(layer_ref);
	hza.style.display = m_state;
    }
} 