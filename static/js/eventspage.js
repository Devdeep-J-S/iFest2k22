const btn=document.querySelectorAll('.btn');

for(let i=0;i<btn.length;i++)
{
    if((i%2)==0)
        btn[i].style.backgroundColor="#004D40";
}