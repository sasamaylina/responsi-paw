from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Campaign, Donation
from app.forms import CampaignForm, UserEditForm

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator untuk memastikan hanya admin yang bisa akses"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def dashboard():
    total_users = User.query.count()
    total_campaigns = Campaign.query.count()
    total_donations = Donation.query.count()
    total_collected = db.session.query(db.func.sum(Donation.amount)).scalar() or 0
    
    recent_donations = Donation.query.order_by(Donation.created_at.desc()).limit(5).all()
    active_campaigns = Campaign.query.filter_by(is_active=True).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          title='Admin Dashboard',
                          total_users=total_users,
                          total_campaigns=total_campaigns,
                          total_donations=total_donations,
                          total_collected=total_collected,
                          recent_donations=recent_donations,
                          active_campaigns=active_campaigns)


# ==================== CAMPAIGN CRUD ====================

@admin_bp.route('/campaigns')
@admin_required
def campaigns():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template('admin/campaigns.html', title='Kelola Campaign', campaigns=campaigns)


@admin_bp.route('/campaigns/create', methods=['GET', 'POST'])
@admin_required
def create_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            title=form.title.data,
            description=form.description.data,
            target_amount=form.target_amount.data,
            is_active=form.is_active.data
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign berhasil dibuat!', 'success')
        return redirect(url_for('admin.campaigns'))
    
    form.is_active.data = True
    return render_template('admin/campaign_form.html', title='Buat Campaign', form=form, is_edit=False)


@admin_bp.route('/campaigns/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    form = CampaignForm(obj=campaign)
    
    if form.validate_on_submit():
        campaign.title = form.title.data
        campaign.description = form.description.data
        campaign.target_amount = form.target_amount.data
        campaign.is_active = form.is_active.data
        db.session.commit()
        flash('Campaign berhasil diperbarui!', 'success')
        return redirect(url_for('admin.campaigns'))
    
    return render_template('admin/campaign_form.html', title='Edit Campaign', form=form, is_edit=True, campaign=campaign)


@admin_bp.route('/campaigns/<int:id>/delete', methods=['POST'])
@admin_required
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign berhasil dihapus!', 'success')
    return redirect(url_for('admin.campaigns'))


# ==================== USER CRUD ====================

@admin_bp.route('/users')
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', title='Kelola User', users=users)


@admin_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)
    
    if form.validate_on_submit():
        # Check if username/email changed and already exists
        if form.username.data != user.username:
            existing = User.query.filter_by(username=form.username.data).first()
            if existing:
                flash('Username sudah digunakan.', 'danger')
                return render_template('admin/user_form.html', title='Edit User', form=form, user=user)
        
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('Email sudah terdaftar.', 'danger')
                return render_template('admin/user_form.html', title='Edit User', form=form, user=user)
        
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User berhasil diperbarui!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', title='Edit User', form=form, user=user)


@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Anda tidak bisa menghapus akun sendiri!', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus!', 'success')
    return redirect(url_for('admin.users'))


# ==================== DONATIONS READ ====================

@admin_bp.route('/donations')
@admin_required
def donations():
    donations = Donation.query.order_by(Donation.created_at.desc()).all()
    return render_template('admin/donations.html', title='Semua Donasi', donations=donations)
